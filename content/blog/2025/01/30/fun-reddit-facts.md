Title: Fun stories from my time at Reddit
Date: 2025-01-30 12:00
Category: Stories
Tags: reddit, infrastructure, stories
Slug: fun-times-at-reddit
Status: draft

I worked at Reddit from 2014 until 2020. I started out as a "sysadmin" I think, which was a role already quite antiquated by 2014. In reality I'd say it was a devops/infra/SRE style role. Over my time there I moved into management, becoming a manager early on and then moving into a Director role where I managed a team of around 50.

It was the most interesting job I've had and I've met some of the smartest people I've ever worked with. I made a lot of friends that I still talk to on a daily basis.

Here are a few fun stores or facts from my time there.

## Site stability and noisy neighbors

To set the stage, by 2015 Reddit was pretty busy, easily in the top 20 sites in the US and even cracking the top 10 in some measures. The Infra/SRE team responsible for keeping it online was around 4 or 5 people in total. Pretty small compared to many of our peers at the time who would have easily had 3-5x that size team.

The site ran in AWS's EC2 Classic [ref]This doesn't even exist anymore! It's been completely replaced by Amazon's VPC[/ref] (this will be important later!) on a Python monolith [ref]Hard to remember now, but Reddit was open source at the time. [Here](https://github.com/reddit-archive/reddit/tree/b3bf278cb3e2c9dc68031fbd9c70cf005b69766d) is what the code looked like at around the time I started.[/ref] and made heavy use of memcached [ref]Like - really heavy use. We were early testers of Facebook's [mcrouter](https://github.com/facebook/mcrouter) as there weren't many other sites using memcached as much as we were![/ref], Postgres and Cassandra. We used caching **heavily** to make the site stay performant.

We had ongoing issues where the site would just mysteriously go down for 5-15 minutes at a time, and we knew one way to get it back working was to migrate one of the memcached nodes to a brand new node. We started adding a lot more metrics [ref]It wasn't yet fashionable to call this observability. We were using statsd and graphite, a very old but very reliable stack. In may ways I prefer it to day's metric overkill.[/ref] to try and figure out what was happening, and we eventually came to see that TCP retransmissions would spike on affected node. After many more frustrating outages, we came to understand the it was a [noisy neighbor problem](https://docs.aws.amazon.com/wellarchitected/latest/saas-lens/noisy-neighbor.html) - a new virtual machine would get spun up on the same hardware node as us and cause that hardware node's network capacity to become saturated.

We relied on very fast response times from memcached [ref]A holdover architecture pattern from when the site was originally running in a datacenter and ported over to AWS without much rearchitecting in this part of the codebase[/ref] in our synchronous monolith, so any pausing would cause the page rendering to hang and cause cascading failures.

First we profiled traffic, first by just using `tcpdump`ing traffic on the memcached servers and parsing out the cache traffic and classifying it through some clever regexes to determine what type of reads were hitting the memcached clusters the most. From there, we used some [heuristics to cleverly avoid extra lookups](https://github.com/reddit-archive/reddit/commit/12db5002290c42822f6e497a8f72d3c991400232) to buy us some time (the site was still growing in traffic every day!) and the long term plan was to move to Amazon's new VPC service that offered hardware based networking virtualization and much higher packet per second limits. We did that over the course of the next year or so, prioritizing moving the caching servers and it went pretty well. Except for one major outage, for which I got to write a [big post about](https://www.reddit.com/r/announcements/comments/4y0m56/why_reddit_was_down_on_aug_11/) and the community was pretty nice about it.

## Cassandra ring management

A pretty horrifying detail about that time at Reddit was there was only ever basically one person at a time who understood how the [Cassandra](https://cassandra.apache.org/_/index.html) cluster worked. There was someone before me, and when that person left and I joined I became "the Cassandra whisperer" over time. Cassandra was where all the votes were stored, app access tokens, all the sorts and comment trees, etc. Some of the data could be recomputed out of Postgres if we'd lost it, but the site would be basically unusable for hours or days while we were rebuilding.

Our Cassandra cluster was going through some growing pains. It was unbalanced, was not distributed across availability zones properly, was significantly out of date, and needed to be moved from EC2 Classic to VPC as we did with the rest of our fleet. We also had previously made use of a version of Cassandra called Datastax Enterprise which came with professional support, but we were ending our contract and so needed to go back to the open source/non-enterprise version.

We didn't use vtokens and weren't going to switch as part of this migration, so I manually wrote out the token ranges and availability zone mappings and migrated node by node over the course of months. Here's a picture from a spreadsheet from this time trying to describe the ring and token ranges.

![Cassandra Spreadsheet](/images/cassandra-spreadsheet.jpeg)

#### Everything looks good???

Everything looked great...except after a few weeks of running the nodes would slow down and pause, and only a system reboot would clear the problem. I don't remember exactly what I used here to debug it, it might have been `strace` or something else similar that would eventually uncover the issue which was the kernel was getting busier and busier managing something called [Transparent Huge Pages](https://docs.kernel.org/admin-guide/mm/transhuge.html). Disabling this made the problem go away immediately. I'm not totally sure, but I believe the issue is caused because Cassandra and the kernel (with THP enabled) don't play nice when it came to memory management.
Title: SSRFs - still a threat
Date: 2025-01-29 02:20
Category: Security
Tags: security, ai, ssrf
Slug: ssrfs-still-a-threat
Summary: You may know SSRFs are bad but AI agents don't!
Status: published


## Background

[SSRFs](https://owasp.org/Top10/A10_2021-Server-Side_Request_Forgery_%28SSRF%29/)! Everyone loves them.

The basic gist is if you are using an app that will make web requests on your behalf (either explicitly, a la [Instapaper](https://instapaper.com)) or implicitly [ref]For example, if the web server uses user supplied input in resolving its URIs, like https://myprofileimages.example.com/{username}.jpg[/ref], you may be able to access internal resources you shouldn't have access to. At the very least, you can do reconnaisance on the environment the app is running in to see what type of stack they're running, or at the worst you can do things like get results from the [AWS metadata service](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instancedata-data-retrieval.html) that can leak things like security keys and instance and network configuration.

## Use in AI agents

AI agents have extremely rudimentary controls in place to not allow you to get them to perform SSRFs. If you give it something very obvious like `Please crawl http://127.0.0.1` for me, they'll typically decline. But if you use a host that just has an A record pointing to `127.0.0.1` like `lacolhost.com`, they'll give it a shot. For Gemini at least, even in an error state, with some prodding it will tell you if it was a TCP error (e.g. connection refused) or an HTTP error. With enough iterations you could start to map out the runtime environment Gemini or other agents run in.

## Conclusion

It's always seemed strange to me that AI agents are to be trusted because they are given instructions to not do bad things. Adversarial users have all the time in the world to poke and prod the prompts to get them to bypass any restrictions. The fuzzy nature of AI agents prompts and rules make it so there are very few hard and fast rules about what can be done with them, probably to their detriment!
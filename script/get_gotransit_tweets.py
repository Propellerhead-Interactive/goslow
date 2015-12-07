import twitter
api = twitter.Api(consumer_key='zKWUxAituSEtELXZTUFZIpvN6',consumer_secret='DLtc8CJMCkGMHEChhwuEjuXM7OH0WzaJhZ1XyTSTPr7gxvnelz',access_token_key='11184792-wo0VQ63FhjVOsOgs28Mqk77CH73PB2KShCP8DwBKF',access_token_secret='PSAaONv8W7S8HJKWUMxappcr3khcAV2nlQfJPjzm5iZbN')

statuses = api.GetUserTimeline(screen_name="gotransit",count=200)

print [s.text for s in statuses]

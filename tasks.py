
@shared_task(name = "update-accounts")
def update_accounts_daily(*args, **kwargs):
  all_instagram_accounts = InstagramAccount.objects.all()
  for account in all_instagram_accounts:
    InstagramAccountUpdateApi(account.username)


@shared_task(name = "update-competitors_account")
def update_competitor_accounts_daily(*args, **kwargs):
  all_instagram_accounts = CompetitorAccount.objects.all()
  for account in all_instagram_accounts:
    CompetitorAccountUpdateApi(account.username)


@shared_task(name = "update-posts-week")
def update_posts_last_week(*args, **kwargs):
  all_instagram_accounts = InstagramAccount.objects.all()
  for account in all_instagram_accounts:
    InstagramAccountPostWeekCloneApi(account.username)
  

@shared_task(name='update-competitor-posts-week')
def update_competitor_posts_last_week(*args, **kwargs):
  all_instagram_accounts = CompetitorAccount.objects.all()
  for account in all_instagram_accounts:
    CompetitorInstagramPostWeekUpdateApi(account.username)


def InstagramAccountUpdateApi(username):
  params = getCreds()
  response = getAccount(params, username)
  if 'business_discovery' in response['json_data']:
    account_json = response['json_data']['business_discovery']
    instagram_account = InstagramAccount.objects.filter(username=username).first()
    startdate = date.today()
    enddate = startdate + timedelta(days=1)
    if DailyInstagramAccount.objects.filter(instagram_account=instagram_account).filter(created__range=[startdate, enddate]).count()>0:
      today_account = DailyInstagramAccount.objects.filter(instagram_account=instagram_account).filter(created__range=[startdate, enddate]).first()
      today_account.total_followers = account_json['followers_count']
      instagram_account.name = account_json['name']
      instagram_account.followers = account_json['followers_count']
      instagram_account.following = account_json['follows_count']
      instagram_account.posts = account_json['media_count']
      if 'biography' in account_json:
        instagram_account.bio = account_json['biography']
      if 'website' in account_json:
        instagram_account.website = account_json['website']
      instagram_account.get_image_from_url(account_json['profile_picture_url'])
      instagram_account.save()
    else:
      DailyInstagramAccount.objects.create(instagram_account=instagram_account,
      total_followers=account_json['followers_count'])
      instagram_account.name = account_json['name']
      instagram_account.followers = account_json['followers_count']
      instagram_account.following = account_json['follows_count']
      instagram_account.posts = account_json['media_count']
      if 'biography' in account_json:
        instagram_account.bio = account_json['biography']
      if 'website' in account_json:
        instagram_account.website = account_json['website']
      instagram_account.get_image_from_url(account_json['profile_picture_url'])
      instagram_account.save()


def CompetitorAccountUpdateApi(username):
  params = getCreds()
  response = getAccount(params, username)
  if 'business_discovery' in response['json_data']:
    account_json = response['json_data']['business_discovery']
    instagram_account = CompetitorAccount.objects.filter(username=username).first()
    startdate = date.today()
    enddate = startdate + timedelta(days=1)
    if DailyCompetitorAccount.objects.filter(instagram_account=instagram_account).filter(created__range=[startdate, enddate]).count()>0:
      today_competitor = DailyCompetitorAccount.objects.filter(instagram_account=instagram_account).filter(created__range=[startdate, enddate]).first()
      today_competitor.total_followers = account_json['followers_count']
      instagram_account.name = account_json['name']
      instagram_account.followers = account_json['followers_count']
      instagram_account.following = account_json['follows_count']
      instagram_account.posts = account_json['media_count']
      if 'biography' in account_json:
        instagram_account.bio = account_json['biography']
      if 'website' in account_json:
        instagram_account.website = account_json['website']
      instagram_account.get_image_from_url(account_json['profile_picture_url'])
      instagram_account.save()
    else:
      DailyCompetitorAccount.objects.create(instagram_account=instagram_account,
      total_followers=account_json['followers_count'])
      instagram_account.name = account_json['name']
      instagram_account.followers = account_json['followers_count']
      instagram_account.following = account_json['follows_count']
      instagram_account.posts = account_json['media_count']
      if 'biography' in account_json:
        instagram_account.bio=account_json['biography']
      if 'website' in account_json:
        instagram_account.website = account_json['website']
      instagram_account.get_image_from_url(account_json['profile_picture_url'])
      instagram_account.save()


def InstagramAccountPostWeekCloneApi(username):
  params = getCreds()
  response = getMedia(params, username)
  if 'business_discovery' in response['json_data']:
    posts_json = response['json_data']['business_discovery']['media']['data']
    last_week = datetime.now().date() - timedelta(days=7)
    for post in posts_json:
      timestamp_date = datetime.strptime(post['timestamp'][0:10], '%Y-%m-%d')
      if timestamp_date.date()<last_week:
          continue
      post_account = InstagramAccountPost.objects.filter(media_id=post['id']).first()
      if post_account != None:
        post_account.comments = post['comments_count']
        post_account.likes = post['like_count']
        post_account.post_date = post['timestamp_date']
        post_account.caption = post['caption']
        if post['media_type']=='IMAGE' or post['media_type']=='CAROUSEL_ALBUM':
            post_account.get_image_from_url(post['media_url'])
        if 'media_url' in post:
          if post['media_type']=='VIDEO':
            post_account.get_image_from_video(post['media_url'])
        post_account.save() 
      else:
        account_instance = InstagramAccount.objects.filter(username=username).first()
        post_account = InstagramAccountPost.objects.create(instagram_account=account_instance,
        post_date=timestamp_date, media_type=post['media_type'], permalink=post['permalink'], media_id=post['id'], caption=post['caption'])
        post_account.comments = post['comments_count']
        if 'like_count' in post:
          post_account.likes = post['like_count']
        if post['media_type']=='IMAGE' or post['media_type']=='CAROUSEL_ALBUM':
          post_account.get_image_from_url(post['media_url'])
        if 'media_url' in post:
          if post['media_type']=='VIDEO':
            post_account.get_gif_from_video(post['media_url'])
        else:
          post_account.copyright_label = True
        post_account.save()


def CompetitorInstagramPostWeekUpdateApi(username):
  params = getCreds()
  response = getMedia(params, username)
  print(response['json_data'])
  if 'business_discovery' in response['json_data']:
    posts_json = response['json_data']['business_discovery']['media']['data']
    last_week = datetime.now().date() - timedelta(days=7)
    for post in posts_json:
      timestamp_date = datetime.strptime(post['timestamp'][0:10], '%Y-%m-%d')
      if timestamp_date.date()<last_week:
          continue
      post_account = CompetitorAccountPost.objects.filter(media_id=post['id']).first()
      if post_account != None:
        post_account.comments = post['comments_count']
        post_account.likes = post['like_count']
        post_account.post_date = post['timestamp_date']
        post_account.caption = post['caption']
        if post['media_type']=='IMAGE' or post['media_type']=='CAROUSEL_ALBUM':
          post_account.get_image_from_url(post['media_url'])
        if 'media_url' in post:
          if post['media_type']=='VIDEO':
            post_account.get_image_from_video(post['media_url'])
        post_account.save() 
      else:
        account_instance = CompetitorAccount.objects.filter(username=username).first()
        post_account = CompetitorAccountPost.objects.create(instagram_account=account_instance,
        post_date=timestamp_date, media_type=post['media_type'], permalink=post['permalink'], media_id=post['id'], caption=post['caption'])
        post_account.comments = post['comments_count']
        if 'like_count' in post:
          post_account.likes = post['like_count']
        if post['media_type']=='IMAGE' or post['media_type']=='CAROUSEL_ALBUM':
          post_account.get_image_from_url(post['media_url'])
        if 'media_url' in post:
          if post['media_type']=='VIDEO':
            post_account.get_gif_from_video(post['media_url'])
        else:
          post_account.copyright_label = True
        post_account.save()
 

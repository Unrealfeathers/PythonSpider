import Get_Atlas
from random_user_agent.user_agent import UserAgent

UA = UserAgent()

url = "https://space.bilibili.com/195413/article"
file_path = "."
Headers = {
        # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)
        # Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.183"
        "User-Agent": UA.get_random_user_agent()
 }

atlas = Get_Atlas.Atlas(file_path=file_path)
atlas.get_url(up_url=url)

get_image = Get_Atlas.Image(file_path=file_path)
get_image.get_images(num=30, headers=Headers)

import Get_Atlas

url = "https://space.bilibili.com/195413/article"
file_path = "."

atlas = Get_Atlas.Atlas(up_url=url, file_path=file_path)
# noinspection PyBroadException
try:
    atlas.get_url()
except Exception:
    print("Error\n")

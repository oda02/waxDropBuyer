from ScreenManager import CheckImage

finder = CheckImage()
finder.upload_image('main.png')
print(finder.find_image('mine1.png'))
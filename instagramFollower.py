from selenium import webdriver
from time import sleep
from creditentials import username, password


class igBot:
    def __init__(self, username, password):
        self.driver = webdriver.Chrome()
        self.username = username
        self.driver.get("https://instagram.com")
        sleep(2)
        self.driver.find_element_by_xpath("//input[@name=\"username\"]").send_keys(username)
        self.driver.find_element_by_xpath("//input[@name=\"password\"]").send_keys(password)
        self.driver.find_element_by_xpath('//button[@type="submit"]').click()
        sleep(6)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()
        sleep(2)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()
        sleep(2)

    def getUnfollowers(self):
        self.driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format(self.username)).click()
        sleep(3)
        self.driver.find_element_by_xpath("//a[contains(@href,'/following')]").click()
        following = self.getNames()
        self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]").click()
        followers = self.getNames()
        not_following_back = [user for user in following if user not in followers]
        self.notFollowing = not_following_back
        self.eraseUser()
        print(not_following_back)

    def eraseUser(self):
        for usr in self.notFollowing:
            self.driver.find_element_by_xpath("//input[@placeholder=\"Search\"]").send_keys(usr)
            sleep(5)
            self.driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format(usr)).click()
            sleep(5)
            #The next selector occasionally needs to be changed up as IG changes
            self.driver.find_element_by_xpath("//*[@id=\"react-root\"]/section/main/div/header/section/div[1]/div[2]/span/span[1]/button").click()
            sleep(5)
            self.driver.find_element_by_xpath("//button[contains(text(), 'Unfollow')]").click()
            sleep(10)

    def getNames(self):
        sleep(2)
        scrollBox = self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div[2]")
        prev_height, height = 0, 1
        while prev_height != height:
            prev_height = height
            sleep(3)
            height = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                return arguments[0].scrollHeight;
                """, scrollBox)
        links = scrollBox.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']
        self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div[1]/div/div[2]/button").click()
        return names


notBot = igBot(username, password)
try:
    notBot.getUnfollowers()
    notBot.driver.close()
except:
    notBot.driver.close()

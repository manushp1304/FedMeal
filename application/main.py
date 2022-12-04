import pygame,sys,time, random
pygame.init()

screenWidth = 800
screenHeight = 700
screen = pygame.display.set_mode((screenWidth ,screenHeight),0)

WHITE = (255,255,255)                   #colour rgbs
BLACK = (0,0,0)
RED = (253, 53, 64)
GREEN = (0,255,0)	
BLUE = (0,0,255)
GREY = (211,211,211)

logowidth = 400                         #Starting Screen Variables                
logoheight = 300
buttonWidth = 180
buttonHeight = 50
buttonSpace = 10

introTextFont = pygame.font.SysFont("Roboto", 30)       #fonts
loginRegFont = pygame.font.SysFont("Roboto", 100)
promptFont = pygame.font.SysFont("Roboto", 30)
nameFont = pygame.font.SysFont("Arial", 16)
priceFont = pygame.font.SysFont("Arial", 12)
subHeadingFont = pygame.font.SysFont("Arial",38)
u_base_font = pygame.font.Font(None,32)
p_base_font = pygame.font.Font(None,32)

user_text = ''
pass_text = ''
usernames = []
passwords = []
addressList = []
cardnumList = []
incorrectInfo = False
foodList = [["pizza.jpg","Pizza",12.99],["burger.jpg","Burger",5.99],["fries.jpg","Fries",2.99],["onionring.jpg","Onion Rings",2.99],["drink.jpg","Shirley Temple",7.99],["pasta.jpg","Pasta",9.99],["spaghetti.jpg","Spaghetti",9.99],["burrito.jpg","Burrito",6.99],["burritobowl.jpg","Burrito Bowl",6.99]]  #2D List to store product name, price, and image url
foodRectList = []
                                                  #selection and billing variables
clicked = False
selected = False
totalItems = 0
orderList = []
count = 0
quantityList = []
subtotal = 0
newList = []
total = True
finalHeadings = ["Subtotal","Sales Tax(13%)","Total"]
generateReciept = False
recieptNumber = 0
userIndex,passIndex = (0,0)
                                                  #colour selection variables
color_active = BLUE
color_passive = (211,211,211)
u_color = color_passive
p_color = color_passive
u_active = False
p_active = False

condition = 1
pressed = False

screen.fill(WHITE)
pygame.display.update()

boxRect = pygame.Rect(100,100,100,100)                                           #all rects
logoVar = pygame.image.load("logo.png")
logoVar = pygame.transform.scale(logoVar, (logowidth, logoheight))
logoRect = logoVar.get_rect()
logoRect.center = (screenWidth//2,(screenHeight//2)-100)
usernameRect = pygame.Rect(screenWidth//2,screenHeight//3,200,32)
passwordRect = pygame.Rect(screenWidth//2,screenHeight//2,200,32)
loginRect = pygame.Rect(screenWidth//2 - (buttonWidth+buttonSpace), screenHeight//2+100, buttonWidth, buttonHeight)
registerRect = pygame.Rect(screenWidth//2 + buttonSpace, screenHeight//2+100, buttonWidth, buttonHeight)
submitRect = pygame.Rect(screenWidth//2 - buttonWidth//2,screenHeight//1.5, buttonWidth, buttonHeight)
continueRect = pygame.Rect(screenWidth//2 - buttonWidth//2,screenHeight//1.5, buttonWidth, buttonHeight)
enterRect = pygame.Rect(screenWidth//2 - buttonWidth//2,screenHeight//1.35, buttonWidth, buttonHeight)
clearRect = pygame.Rect(80,screenHeight-80,120,buttonHeight)
checkoutRect = pygame.Rect(0,screenHeight-80,130,buttonHeight)
nextRect = pygame.Rect(0,screenHeight-80,130,buttonHeight)
declineRect = loginRect = pygame.Rect(screenWidth//2 - (buttonWidth+buttonSpace), screenHeight-150, buttonWidth, buttonHeight)
confirmRect = registerRect = pygame.Rect(screenWidth//2 + buttonSpace, screenHeight-150, buttonWidth, buttonHeight)


def intro_Text(buttonText,introTextFont,square):              #function creates text for 2 buttons - login and register
  introText = introTextFont.render(buttonText,True,WHITE)     #render text
  introTextRect = introText.get_rect()                        #create rect
  introTextRect.center = (square.center)                      #center it in surround box
  screen.blit(introText, introTextRect)                       #blit it onto the screen

def login_reg_submit(title,font, leftPosition, color, topPosition): #function creates titles for each page
  titleText = font.render(title,True,color)                         #render text
  titleRect = titleText.get_rect()                                  #create rect
  titleRect.center = (leftPosition, topPosition)                    #center it accordingly
  screen.blit(titleText, titleRect)                                  #blit it onto the screen

def user_pass(username, password, font, screenWidth, screenHeight): #function creates prompt text - username and password
  usernameText = font.render(username,True,RED)                     #username
  usernameRect = usernameText.get_rect()
  usernameRect.topleft = (screenWidth//5,screenHeight//3)
  screen.blit(usernameText,usernameRect)

  passwordText = font.render(password,True,RED)                     #password
  passwordRect = passwordText.get_rect()
  passwordRect.topleft = (screenWidth//5,screenHeight//2)
  screen.blit(passwordText, passwordRect)

def input(screen, inputRect, color, base_font, text, color_active, color_passive, active):
  pygame.draw.rect(screen,color,inputRect,2)                        #anything typed into the input field becomes the text to be rendered and blitted
  text_surface = base_font.render(text,True,color)
  screen.blit(text_surface, (inputRect.x+5,inputRect.y+5))
  inputRect.w = max(200,text_surface.get_width() + 10)              #the input box will either be 200px or larger depending on how much you type
  if active:                                                        #when hovered, color becomes red
    color = RED
  else:
    color = GREY
  return color,text                                                 #return the color and text back into the program

def createImage(food, width, height, x, y):                         #function generates images for all food items
  imageVar = pygame.image.load(food)
  imageVar = pygame.transform.scale(imageVar,(width,height))
  imageRect = imageVar.get_rect()
  imageRect.left = x
  imageRect.top = y
  x += 240                                                          #the images shifts 240 pixels horizontally after each image
  screen.blit(imageVar,imageRect)                                   #blit the image
  return imageRect                                                  #return the rect

def createLabel(name, font, x, y):                                  #function creates product title and price
  nameText = font.render(name,True,BLACK)                           #renders text, creates rect, centers rect, and blits it onto screen
  nameRect = nameText.get_rect()
  nameRect.center = (x,y)
  screen.blit(nameText, nameRect)
  return nameRect                                                   #returns that rect

def createRect(imageRect, boxRect, color, nameRect):                
  boxRect.x = imageRect.left
  boxRect.y = imageRect.top
  boxRect.width = imageRect.width
  boxRect.height = imageRect.height + nameRect.bottom - imageRect.bottom
  pygame.draw.rect(screen,color,boxRect,2)

def final_order(item,x,y, font):                                    #function generates red box around product when hovered with mouse
  itemText = font.render(item,True,BLACK)                           #render text, create rect, center rect, blit it onto screen
  itemRect = itemText.get_rect()
  itemRect.topleft = (x,y)
  screen.blit(itemText,itemRect)
  
  

go = True
while go:                                                           #main loop
  for event in pygame.event.get():            
    if event.type == pygame.QUIT:
      go = False
    if event.type == pygame.KEYDOWN:                                #when any key on the keyboard is down
      if u_active:
        if event.key == pygame.K_BACKSPACE:                         #delete text from input field on backspace
          user_text = user_text[:-1]
        elif event.key == pygame.K_RETURN:                          #leave the input field when enter is pressed
          u_active = False
          usernameValue = user_text                                 #store the value in the input field
        else:
          user_text += event.unicode                                #if not backspace or enter, add the value of the key(a,b,c,d...) to a variable
      if p_active:                                                  #same concept for password
        if event.key == pygame.K_BACKSPACE:                         #backspace deletes last key
          pass_text = pass_text[:-1]
        elif event.key == pygame.K_RETURN:                          #enter leaves the input field
          p_active = False
          usernameValue = user_text                                 #stores whatever is in the input field in a variable
        else:
          pass_text += event.unicode                                #if not backspace or enter, any other key will be added to the word
      if event.key == pygame.K_SPACE and condition == 5:            #if space is pressed on page 5, direct user to page 6
          condition = 6
      if event.key == pygame.K_r and condition == 9:                #if r key is pressed on page 9
        totalItems = 0                                              #clear cart
        total = True                                                #reset variable for next order
        generateReciept = True                                      #generate the reciept of this order
        condition = 10                                              #direct user to page 10
        clicked = False                                              
    if event.type == pygame.MOUSEBUTTONDOWN:                        
      if loginRect.collidepoint(event.pos) and condition == 1:      #on the start up page if login is pressed
        condition = 2                                               #redirect to login page(page #2)
      elif registerRect.collidepoint(event.pos) and condition == 1: #if register option is chosen
        condition = 3                                               #redirect to register page(page #3)
      if usernameRect.collidepoint(event.pos):                      #if username input field is clicked
        u_active = True                                             #set username active to true so red box is created around the input text field on click
        p_active = False                                            #the red box around password input field will deactivate
      elif passwordRect.collidepoint(event.pos):                    #same for password input field
        p_active = True                                             #when password input field is clicked, password red box is activated
        u_active = False                                            #username red box is deactivated
      else:
        u_active = False                                            #if neither input field is chosen, deactivate both
        p_active = False
      if submitRect.collidepoint(event.pos) and condition == 2:     #if submit is clicked from login page
        usernameValue = user_text                                   #store the values in the input text field
        passwordValue = pass_text
        incorrectInfo = False
        if usernameValue in usernames and passwordValue in passwords: #if both username and password are in the memory of the program
          userIndex = usernames.index(usernameValue)                #get the index of that username and password in the list of usernames and passwords
          passIndex = passwords.index(passwordValue)
          if userIndex == passIndex:                                #if the username and password have the same index number/belong to a user
            currentAddress = addressList[userIndex]                 #pull out the address and card number associated with the index number
            currentCardNum = cardnumList[userIndex]
            condition = 5                                           #redirect to next page
            userIndex,passIndex = (0,0)                             #reset index values for next login
          else:
            incorrectInfo = True                                    #if username or password is incorrect, write an error message on screen
            user_text = ''                                          #reset both input text fields
            pass_text = ''
            userIndex,passIndex = (0,0)                             #reset indexes for next login
        else:
          incorrectInfo = True                                      #if username or password is not in the database, output and error message
          user_text = ''                                            #clear input text fields
          pass_text = ''
          userIndex,passIndex = (0,0)                               #reset indexes
        
      if continueRect.collidepoint(event.pos) and condition == 3:   #if cotinue is clicked on page #register page
        usernameValue = user_text                                   #store the values in username and password text fields
        passwordValue = pass_text
        user_text = ''                                              #clear the input text fields
        pass_text = ''
        if usernameValue in usernames:                              #if user exists under same username
          incorrectInfo = True                                      #output error message
        else:                                                       #if there is no user under same username, continue with the program
          usernames.append(usernameValue)                           #append the username value into usernames list
          passwords.append(passwordValue)                           #append the password value into passwords list
          condition = 4                                             #move onto next page(page #4)
          incorrectInfo = False

      if enterRect.collidepoint(event.pos) and condition == 4:      #when enter is pressed when registering - address and card number
        newAddress = user_text                                      #store the new address
        newCardNum = pass_text                                      #store the new card number
        user_text = ''                                              #clear the input text fields
        pass_text = ''
        if newCardNum.isdigit():                                    #check if the card number is a digit
          addressList.append(newAddress)                            #append new address to addresslist
          cardnumList.append(newCardNum)                            #append  new card number to cardNumList
          condition = 5                                             #redirect to page #5
          incorrectInfo = False                                     
        else:
          incorrectInfo = True                                      #if card number is not a digit, output and error message
        
      if condition == 6:                                            #when mouse button is pressed on page 6, computer will check if the mouse position is in a product
        clicked = True
      if clearRect.collidepoint(event.pos) and condition == 6:      #when the clear cart button is pressed
        totalItems = 0                                              #clear cart
        clicked = False                                             #nothing is selected
        orderList = []                                              #clear the entire order list
      if checkoutRect.collidepoint(event.pos) and condition == 6:   #when checkout button is pressed on page 6,
        condition = 7                                               #redirect to next page(Summary Page)
      if nextRect.collidepoint(event.pos) and condition == 7:       #when next button is pressed on page 7,
        condition = 8                                               #redirect to next page(Page #8)
      
      if confirmRect.collidepoint(event.pos) and condition == 8:    #when confirm is pressed on page #8
        condition = 9                                               #redirect to Page #9
      if declineRect.collidepoint(event.pos) and condition == 8:    #if decline is pressed on page #8
        condition = 5                                               #redirect to page #5
        orderList = []                                              #clear order list
        totalItems = 0                                              #clear cart
        subtotal = 0                                                #clear the total amount
        total = True                                                #ready for new order
        clicked = False
      
  if condition == 1:                                                #on first page
    screen.fill(WHITE)                                              #reset the screen
    user_text = ''                                                  #clear the input text fields - username and password
    pass_text = ''  
    pygame.draw.rect(screen,RED,loginRect,0)                        #draw login and register buttons
    pygame.draw.rect(screen,RED,registerRect,0)
    intro_Text("LOGIN",introTextFont,loginRect)                     #put text into the button
    intro_Text("REGISTER",introTextFont, registerRect)
    screen.blit(logoVar, logoRect)                                  #blit the logo onto the screen

  if condition == 2:                                                #on login page
     screen.fill(WHITE)                                             #reset screen
     login_reg_submit("LOGIN",loginRegFont, screenWidth//2, RED, 80)        #create login title
     user_pass("USERNAME: ","PASSWORD: ", promptFont,screenWidth,screenHeight)      #create input prompts
     userVar = input(screen, usernameRect, u_color, u_base_font, user_text, color_active, color_passive, u_active)        #create input text field for username and store returned values - color and text
     u_color = userVar[0]
     passVar = input(screen, passwordRect, p_color, p_base_font, pass_text, color_active, color_passive, p_active)        #create input text field for password and store returned values - color and text
     p_color = passVar[0]
     pygame.draw.rect(screen, RED, submitRect, 0)                                                                         #draw submit button
     login_reg_submit("SUBMIT",promptFont, submitRect.centerx, WHITE, submitRect.centery)                                 #create text to put in submit button
     if incorrectInfo:                                                                                                    #if not such user
       incorrectText = promptFont.render("Invalid Info. No Such User",True,RED)                                           #output error message
       incorrectRect = incorrectText.get_rect()
       incorrectRect.center = (screenWidth//2,submitRect.bottom + 30)
       screen.blit(incorrectText,incorrectRect)                                                                           #blit the message onto screen

  if condition == 3:                                                #on register page
     screen.fill(WHITE)                                             #clear the screen
     login_reg_submit("REGISTER",loginRegFont, screenWidth//2, RED, 80)                                                   #create page title
     user_pass("USERNAME: ","PASSWORD: ", promptFont,screenWidth,screenHeight)                                            #create input prompts
     userVar = input(screen, usernameRect, u_color, u_base_font, user_text, color_active, color_passive, u_active)        #create input text field for username and store returned values - color and text
     u_color = userVar[0]                 
     passVar = input(screen, passwordRect, p_color, p_base_font, pass_text, color_active, color_passive, p_active)        #create input text field for password and store returned values - color and text
     p_color = passVar[0]
     pygame.draw.rect(screen, RED, continueRect, 0)                                                                       #draw continue button
     login_reg_submit("CONTINUE",promptFont, continueRect.centerx, WHITE, continueRect.centery)                           #create text to put in button
     if incorrectInfo:                                                                                      #if username already exists
       incorrectText = promptFont.render("Invalid. User already exists",True,RED)                           #output error message
       incorrectRect = incorrectText.get_rect()
       incorrectRect.center = (screenWidth//2,continueRect.bottom + 30)
       screen.blit(incorrectText,incorrectRect)                                                             #blit message onto screen

  if condition == 4:                                               #on register page - part 2
    screen.fill(WHITE)
    login_reg_submit("REGISTER",loginRegFont, screenWidth//2, RED, 80)                                                    #create page title
    user_pass("ADDRESS: ","CARD NO.: ", promptFont,screenWidth,screenHeight)                                              #create input prompts
    userVar = input(screen, usernameRect, u_color, u_base_font, user_text, color_active, color_passive, u_active)         #create input text field for address and store returned values - color and text
    u_color = userVar[0]
    currentAddress = userVar[1]                                                                                           #set input to current address
    passVar = input(screen, passwordRect, p_color, p_base_font, pass_text, color_active, color_passive, p_active)         #create input text field for card number and store returned values - color and text
    p_color = passVar[0]
    currentCardNum = passVar[1]                                                                                           #set input to current card number
    pygame.draw.rect(screen, RED, enterRect, 0)                                                                           #creat enter button
    login_reg_submit("SUBMIT",promptFont, enterRect.centerx, WHITE, enterRect.centery)                                    #create text for the button
    if incorrectInfo:                                                                                                     #if card number is not a digit
       incorrectText = promptFont.render("Invalid. Card Number must be a number",True,RED)                                #output error message
       incorrectRect = incorrectText.get_rect()
       incorrectRect.center = (screenWidth//2,enterRect.bottom + 30)
       screen.blit(incorrectText,incorrectRect)                                                                           #blit message onto screen

  if condition == 5:                                                                                                      #on page #5
    screen.fill(WHITE)                                                                                                    #clear screen
    welcomeText = promptFont.render("Welcome " + usernameValue + "! Press Space to Begin Shopping",True,RED)              #create message for user
    welcomeRect = welcomeText.get_rect()
    welcomeRect.center = (screenWidth//2,screenHeight//2)
    screen.blit(welcomeText,welcomeRect)                                                                                  #blit message

  if condition == 6:                                                                                                      #if on main page
    screen.fill(WHITE)                                                            #clear screen
    x,y = (80,20)                                                                 #set initial x and y
    width,height = (150,120)                                                      #set width and height
    for item in foodList:                                                         #for every item FedMeal offers
      currentImage = createImage(item[0],width,height,x,y)                        #call function and pass image url
      x+=240                                                                      #shift the next image 240 pixels horizontally
      if x+width > 750:                                                           #if the image is almost off the screen
        y += height+70                                                            #shift the image onto the next row and reset the x value
        x = 80
      createLabel(item[1], nameFont, currentImage.centerx, currentImage.bottom+15)                                        #call function and pass product name
      nameRect = createLabel(str(item[2]), priceFont, currentImage.centerx, currentImage.bottom+35)                       #call function and pass product price with a smaller font
      mousePos = pygame.mouse.get_pos()

      if mousePos[0] in range(currentImage.left,currentImage.right) and mousePos[1] in range(currentImage.top,currentImage.bottom+(nameRect.bottom-currentImage.bottom)):             #if mouse position is within a product
        currentboxRect = createRect(currentImage, boxRect, RED, nameRect)         #call function to create red box around product on hover
        if clicked:                                                               #if clicked as well
          totalItems += 1                                                         #increment total items by 1
          orderList.append(item[1])                                               #append item name to order list
          clicked = False                                                         #reset clicked
      totalText = promptFont.render("Total Items: " + str(totalItems),True,RED)                   #output total items in cart
      totalRect = totalText.get_rect()
      totalRect.center = (screenWidth//2,screenHeight-50)
      screen.blit(totalText,totalRect)                                                            #blit it onto screen
      pygame.draw.rect(screen,RED,clearRect,0)                                                    #create clear button 
      intro_Text("CLEAR",introTextFont,clearRect)                                                 #create text to place in button
      pygame.draw.rect(screen,RED,checkoutRect,0)                                                 #create rect for checkout
      intro_Text("CHECKOUT", introTextFont,checkoutRect)                                          #create text for checkout
      checkoutRect.right = screenWidth-80                                                         #set position of button
    
  if condition == 7:                                                          #on summary page
    screen.fill(WHITE)                                                        #clear the screen
    login_reg_submit("Summary",loginRegFont, screenWidth//2, RED, 80)         #create title
    itemy = 100                                                               #set initial y
    for product in foodList:                                                  #for every available product
      itemy += 50                                                             #move down the screen
      quantity = orderList.count(product[1])                                  #count the number of times each product appears in the order list and set that to product quantity
      item = product[1] + " --- " + str(quantity)                             
      final_order(item,20,itemy, promptFont)                                  #output available product onto screen with quantity bought
      subItem = round(product[2]*quantity,2)                                  #calculate the price of each product
      final_order("$" + str(subItem),screenWidth-100,itemy, promptFont)       #output the price for each product
      if total:
        subtotal += subItem                                                   #add the price for each item to the total
    total = False
    subtotal = round(subtotal,2)                                      
    final_order("_________",screenWidth-125,screenHeight-140, promptFont)     #function outputs the subtotal at the botton of page
    final_order("$" + str(subtotal),screenWidth-100,screenHeight-100, promptFont)

    pygame.draw.rect(screen,RED,nextRect,0)                                   #draw next button
    intro_Text("NEXT", introTextFont,nextRect)                                #create text to go in the button
    nextRect.centerx = screenWidth//2                                         #set the position of the button
  
  if condition == 8:                                                          #if on confirmation page
    screen.fill(WHITE)                                                        #clear the screen
    login_reg_submit("Summary",loginRegFont, screenWidth//2, RED, 80)         #create page title

    headingy = 160
    for heading in finalHeadings:                                             #iterate over "subtotal","sales tax", and "total"
      final_order(heading,20,headingy, promptFont)                            #output the heading
      headingy = headingy * 1.3                                               #move down screen
    headingy = 160
    finalPrices = [round(subtotal,2),round(subtotal*0.13,2), round(subtotal*1.13,2)]    #create list of final prices
    for price in finalPrices:
      final_order("$" + str(price),screenWidth-100, headingy, promptFont)     #output the subtotal, sales tax, and final total beside the approriate heading
      headingy = headingy * 1.3                                               #move down the screen
    
    final_order("Card Number: " + currentCardNum,20,350,subHeadingFont)       #confirm card number and shipping address
    final_order("Shipping To: " + currentAddress,20,450,subHeadingFont)

    pygame.draw.rect(screen,RED,declineRect,0)                                #create confirm and decline buttons, and text associate for each button so user can cancel order if shipping address or card number is innaccurate
    pygame.draw.rect(screen,RED,confirmRect,0)
    intro_Text("DECLINE",introTextFont,declineRect)
    intro_Text("CONFIRM",introTextFont, confirmRect)
  
  if condition == 9:                                                          #if order is confirmed
    screen.fill(WHITE)                                                        #clear screen
    thankYouText = promptFont.render("Thank You " + usernameValue + "! Press R to Logout",True,RED)         #output thank you message
    thankYouRect = thankYouText.get_rect()
    thankYouRect.center = (screenWidth//2,screenHeight//2)
    screen.blit(thankYouText,thankYouRect)                                                                      #blit the message onto screen

    if generateReciept:                                                       #generate reciept
      condition = 10
  
  if condition == 10:
    recieptNumber += 1                                                        #increment receipt number for every order placed
    recieptFile = open("reciept# " + str(recieptNumber) + ".txt","w")         #open new file under the reciept number
    recieptFile.write("Order for " + usernameValue + "\n")                    #write order for (the username)
    for product in foodList:                                                  #for every available product
      quantity = orderList.count(product[1])                                  #count how many times that product appears in the order list and set that to quantity
      item = product[1] + " --- " + str(quantity)                             
      subItem = round(product[2]*quantity,2)
      recieptFile.write(item + "   =   " + "$" + str(subItem) + "\n")         #output the product name, quantity, and price for each
    
    recieptFile.write("\n")
    recieptFile.write("Subtotal              ---          $" + str(subtotal) + "\n")                  #output subtotal
    recieptFile.write("Sales Tax             ---          $" + str(round(subtotal*0.13,2)) + "\n")    #output sales tax
    recieptFile.write("Total                 ---          $" + str(round(subtotal*1.13,2)) + "\n")    #output final total

    recieptFile.close()                                                       #close file
    subtotal = 0                                                              #reset total
    orderList = []                                                            #clear order list
    totalItems = 0                                                            #clear cart
    condition = 1                                                             #redirect back to start up page
    total = True                                                              #reset variable for new orders
    clicked = False
    generateReciept = False

  pygame.display.update()                                                     #MOST IMPORTANT ----- display everything onto the screen :)
      

pygame.quit()
sys.exit()

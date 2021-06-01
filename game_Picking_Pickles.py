import pygame
import random
import time
import os.path

pygame.init()

# parametry:
window_size = window_width, window_height = 800, 600
speed = 7
object_limit = 40

#obrazki
ship_file = os.path.join("../game", "rick_ship.png")
explosion_file = os.path.join("../game", "bum.png")
asteroid_file = os.path.join("../game", "asteroid.png")
potato_head_file = os.path.join("../game", "head.png")
pickle_rick_file = os.path.join("../game", "pickle-rick.png")
background_intro = os.path.join("../game", "background.png")
rick_file = os.path.join("../game", "rick.png")

#dzwięki  os.path.join("game","fun.wav")
boom_sound = pygame.mixer.Sound(os.path.join("../game", "boom.wav"))
wubba_sound = pygame.mixer.Sound(os.path.join("../game", "wubba-lubba-dub-dub.wav"))
fun_sound = pygame.mixer.Sound(os.path.join("../game", "fun.wav"))

#kolory
black = (0, 0, 0)
white = (255, 255, 255)
b_blue = (32, 203, 229) 
blue = (23, 118, 143)

# przygotowanie okienka
background = pygame.Surface(window_size)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Picking Pickles!")
clock = pygame.time.Clock()

#________________________________________________________
#_________________FUNKCJE POMOCNICZE_____________________
def display_text(msg, size, x_pos = window_width/2, y_pos = window_height/2, color = white):
    """Funkcja wyświetlająca podany tekst na ekranie. x_pos, y_pos określają położenie środka tego tekstu na ekranie, color to kolor czcionki."""
    
    font = pygame.font.Font(os.path.join("../game", "WickedScaryMovie.ttf"), size)
    text = font.render(msg, True, color)
    rect = text.get_rect()
    rect.center = (x_pos, y_pos)
    screen.blit(text,rect)
    
def game_quit():
    """Funkcja kończąca działanie programu. """
    pygame.quit()
    quit() 
    
def save_best_score(new_score):
    """Funkcja zapisująca najwyższe wyniki do pliku tekstowego. New_score musi być liczbą."""
    with open(os.path.join("../game", "best_score.txt"), "r") as file:
        last_best_scores = file.read().split("#")
    int_scores = [int(score) for score in last_best_scores[:3]]
    int_scores.append(new_score)
    new_best = sorted(int_scores, reverse= True)[:3]  #sortujemy wyniki i odrzucamy najmniejszy i ''
    str_score = f"{new_best[0]}#{new_best[1]}#{new_best[2]}#"
    with open(os.path.join("../game", "best_score.txt"), "w") as updated_file:
        updated_file.write(str_score)

#_________________________________________________________  
#_________________________KLASY___________________________

# Klasy MyShip - gracz
class MyShip(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) # inicjalizacja klasy bazowej
        self.image = pygame.image.load(ship_file) # ładujemy obrazek statku którym będze użytkownik
        self.rect = self.image.get_rect() # pobieramy wymiaru statku
        self.width = self.image.get_width()
        self.rect.center = (window_width /2, window_height* 0.8) # początkowe położenie statku
        self.x_velocity = 0 # początkowa prędkość, można poruszać się tylko w lewo/prawo
        
    def update(self):
        """Funkcja przesuwająca statek gracza. Gdy statek przekroczy granice okienka pojawi się z drugiej strony."""
        self.rect.move_ip((self.x_velocity,0))
        
        if self.rect.left + self.width < 0:  
            self.rect.left = window_width 
        if self.rect.right - self.width > window_width:  
            self.rect.right = 0
            
    def explosion(self):
        """Funkcja wklejająca obrazek wybuchu w miejsce statku."""
        image = pygame.image.load(explosion_file)
        position = self.rect.center[0] - 100, self.rect.center[1] - 120
        screen.blit(image,position)
        pygame.display.update()
        

# Klasa asteroid          
class Asteroid(pygame.sprite.Sprite):
    def __init__(self, img, x_position, y_speed): # inicjalizacja klasy bazowej
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img) # ładujemy grafikę asteroidy
        self.rect = self.image.get_rect()
        self.height = self.image.get_height()
        self.rect.center = (x_position, -self.height) # początkowe położenie statku
        self.y_velocity = y_speed # asteroidy poruszają się  tylko w dół
        
    def update(self):
        """Metoda zmieniająca położenie asteroidy, niszcząca te które już nie znajdują się w obrębie okienka."""
        if self.rect.top > window_height:  
            self.kill()
        else:
            self.rect.move_ip((0,self.y_velocity))
            

# Klasa elementów które gracz zbiera
class CollectItem(pygame.sprite.Sprite):
    def __init__(self, x_position, y_speed):
        pygame.sprite.Sprite.__init__(self)  # inicjalizacja klasy bazowej
        self.image = pygame.image.load(pickle_rick_file)
        self.rect = self.image.get_rect()
        self.height = self.image.get_height()
        self.rect.center = (x_position, -self.height) #początkowe położenie statku
        self.y_velocity = y_speed 
        
    def update(self):
        if self.rect.top > window_height:  
            self.kill()
        else:
            self.rect.move_ip((0,self.y_velocity))
            
# Klasa tablicy wyników          
class ScoreBoard(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.value = 0
        self.text = f"Pickle Ricks: {self.value}"
        self.font = pygame.font.Font(os.path.join("../game", "WickedScaryMovie.ttf"), 40)
        self.image = self.font.render(self.text, True, white)
        self.rect = self.image.get_rect()
        self.rect.topleft = (10,0)
    
    def update(self):
        """Zwiększa wartość wyniku i aktualizuje text i image."""
        self.value += 1    
        self.text = f"Pickle Ricks: {self.value}"
        self.image = self.font.render(self.text,True,white)
        self.rect = self.image.get_rect()
        
        
# Klasa licznika żyć        
class LivesBoard(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.value = 3
        self.text = f"Lives: {self.value}"
        self.font = pygame.font.Font(os.path.join("../game", "WickedScaryMovie.ttf"), 40)
        self.image = self.font.render(self.text, True, white)
        self.rect = self.image.get_rect()
        self.rect.topright = (window_width - 10,0)
    
    def update(self):
        """Zmniejsza liczbę żyć i aktualizuje licznik."""
        self.value += -1    
        self.text = f"Lives: {self.value}"
        self.image = self.font.render(self.text, True, white)
        self.rect = self.image.get_rect()
        self.rect.topright = (window_width - 10, 0)
        
    
# Klasa przycisku   
class MyButton(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, text, i_color, a_color, action=None):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x,y,width, height)
        self.x = x  # położenie lewego górnego rogu przycisku
        self.y = y  
        self.width = width 
        self.height = height 
        self.text = text
        self.i_color = i_color  # podstawowy kolor
        self.a_color = a_color  # kolor zmienia się na jaśnejszy gdy kursor jest nad przyciskiem
        self.action = action  # fukcja przypisana do przycisku
        
    def draw(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, self.a_color, (self.x,self.y,self.width,self.height))
        else:
            pygame.draw.rect(screen, self.i_color, (self.x,self.y,self.width,self.height))
            
        display_text(self.text, 35 , x_pos=(self.x + self.width/2), y_pos=(self.y + self.height/2))
    
    def button_click(self):
        """Funkcja przypisująca działanie do przysicka gdy zostanie on naciśnięty"""
        click = pygame.mouse.get_pressed()
        if self.rect.collidepoint(pygame.mouse.get_pos()): #kursor nad przyciskiem
            if click[0] == 1 and self.text == "PLAY":
                fun_sound.play() # w przypadku wciśnięcia PLAY Rick życzy nam dobrej zabawy
                self.action()
            elif click[0] == 1:
                self.action()


#___________________________________________               
#___________________________________________        

def game_intro():
    """Funkcja ekranu startowego gry."""
    intro = True
    while intro:
        clock.tick(15) 
        for event in pygame.event.get():  
                if event.type == pygame.QUIT:  # sprawdzamy czy użytkownik nie chce wyjśc z programu
                    game_quit()
                    
        image = pygame.image.load(background_intro)
        screen.blit(image,(0,0))
        
        display_text("Picking Pickles", 120, y_pos= window_height *0.25)
        #przysick PLAY
        button_play = MyButton(window_width/2 - 150, window_height*0.45, 300, 50,"PLAY", blue, b_blue, main_loop)
        button_play.draw()
        button_play.button_click()
        #przysick RULES
        button_rules = MyButton(window_width/2 - 150, window_height*0.55, 300, 50,"RULES", blue, b_blue, rules)
        button_rules.draw()
        button_rules.button_click()
        #przysick BEST SCORES
        button_score = MyButton(window_width/2 - 150, window_height*0.65, 300, 50,"BEST SCORES", blue, b_blue, best_scores)
        button_score.draw()
        button_score.button_click()
        #przysick ABOUT AUTHOR
        button_author = MyButton(window_width/2 - 150, window_height*0.75, 300, 50,"ABOUT AUTHOR", blue, b_blue, about_author)
        button_author.draw()
        button_author.button_click()
        #przysick QUIT
        button_quit = MyButton(window_width/2 - 150, window_height*0.85, 300, 50,"QUIT", blue, b_blue, game_quit)
        button_quit.draw()
        button_quit.button_click()
        
        pygame.display.update()
        
        
def rules():
    """Funkcja obsługująca przycisk RULES, wyświetla ekran z zasadami gry."""
    rules_run = True
    while rules_run: 
        clock.tick(15) 
        
        for event in pygame.event.get():  
                if event.type == pygame.QUIT:
                    game_quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: # gdy naciśniemy Esc wrócimy do poprzedniej strony, w tym wypadku głownego menu
                        rules_run = False
                
        screen.fill(black)           
        display_text("Hi, I’m Rick Sanchez from Earth dimension C-137.", 40, y_pos = window_height*0.1)
        display_text("Help me to pick Pickle Ricks but watch out for ", 40, y_pos = window_height*0.2)
        display_text("asteroids and giant heads. I recommend pressing ", 40, y_pos = window_height*0.3)
        display_text("right and left arrows on your keyboard! ", 40, y_pos = window_height*0.4)
        display_text("Good luck and don’t kill us!", 40, y_pos = window_height*0.5)
        display_text("Press  ->  to turn right", 40, y_pos = window_height*0.6)
        display_text("Press  <-  to turn left", 40, y_pos = window_height*0.7)
        display_text("Press  Esc  to go back ", 40, y_pos = window_height*0.8)
        
        image = pygame.image.load(rick_file)
        screen.blit(image, (window_width*0.15, window_height*0.5))
        
        button_play = MyButton(window_width*4.5/8, window_height*0.87, 250, 40,"PLAY", blue, b_blue, main_loop)
        button_play.draw()
        button_play.button_click()  
        
        button_quit = MyButton(window_width*1/8, window_height*0.87, 250, 40, "QUIT",blue, b_blue, game_quit)
        button_quit.draw()
        button_quit.button_click()
    
        pygame.display.update()
        
def best_scores():
    """Funkcja obsługująca przycisk BEST SCORES, wyświetla najlepsze wyniki."""
    score_run = True
    while score_run:  
        clock.tick(15)   
                   
        for event in pygame.event.get():  
                if event.type == pygame.QUIT:
                    game_quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        score_run = False

        with open(os.path.join("../game", "best_score.txt"), "r") as file:
            scores = file.read().split("#")
        
        screen.fill(black)   
        display_text("Your best scores: ", 60, y_pos = window_height*0.2)
        display_text("1.  " + scores[0] + "  Pickle Ricks", 70, y_pos = window_height*0.35)
        display_text("2.  "+scores[1] + "  Pickle Ricks", 70, y_pos = window_height*0.50)
        display_text("3.  "+scores[2] + "  Pickle Ricks", 70, y_pos = window_height*0.65)
        
        button_play = MyButton(window_width*4.5/8, window_height*0.87, 250, 40,"PLAY", blue, b_blue, main_loop)
        button_play.draw()
        button_play.button_click()
        
        button_quit = MyButton(window_width*1/8, window_height*0.87, 250, 40, "QUIT",blue, b_blue, game_quit)
        button_quit.draw()
        button_quit.button_click()
        
        pygame.display.update()
        
        
def about_author():
    """Funkcja obsługująca przycisk ABOUT AUTHOR, wyświetla informacje o autorze."""
    running = True
    while running:   
        clock.tick(15)             
        for event in pygame.event.get():  
                if event.type == pygame.QUIT:
                    game_quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

    
        screen.fill(black)   
        display_text("I'm Kasia Gunia, the author of this extremely ", 45, y_pos = window_height*0.2)
        display_text("complicated game. I'm a first-year student of Applied Maths,", 45, y_pos = window_height*0.3)
        display_text("and as you may suspect I'm a big fan of... "+'"Rick and Morty"!', 45, y_pos = window_height*0.4)
        display_text("So I made a (sophisticated) game about them.", 45, y_pos = window_height*0.5)
        display_text("Unfortunately, nobody pays me for this advert...", 40, y_pos = window_height*0.7)
        
        button_play = MyButton(window_width*4.5/8, window_height*0.83, 250, 40,"PLAY", blue, b_blue, main_loop)
        button_play.draw()
        button_play.button_click()
        
        button_quit = MyButton(window_width*1/8, window_height*0.83, 250, 40, "QUIT",blue, b_blue, game_quit)
        button_quit.draw()
        button_quit.button_click()
        
        pygame.display.update()
        


def main_loop():
    
    #zmienne kontrolne
    running = True
    collect_limit = 1
    add_object = 0
    score = 0
    lives = 3
    
    # inicjalizacja statku gracza
    ship_Sprite = pygame.sprite.RenderClear()
    ship = MyShip()
    ship_Sprite.add(ship)

    # inicjalizacja asteroid
    asteroids_Sprite = pygame.sprite.RenderClear()
    asteroids_Sprite.add(Asteroid(potato_head_file, 500,speed))

    # inicjalizacja CollectItem
    collect_Sprite = pygame.sprite.RenderClear()
    collect_Sprite.add(CollectItem(200, speed))

    # inicjalizacja licznika trafień
    score_Sprite = pygame.sprite.RenderClear()
    score_Sprite.add(ScoreBoard())
    score_Sprite.draw(screen)

    # inicjalizaja licznika żyć
    lives_Sprire = pygame.sprite.RenderClear()
    lives_Sprire.add(LivesBoard())
    lives_Sprire.draw(screen)

    screen.fill(black)
    pygame.display.update()    
    
    while running:
        clock.tick(40)
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:
                save_best_score(score)
                game_quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # naciskając Esc wrócimy do poprzedniego okna
                    save_best_score(score)
                    running = False    
                elif event.key == pygame.K_LEFT:
                    ship.x_velocity = -10 
                elif event.key == pygame.K_RIGHT:
                    ship.x_velocity = 10 
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    ship.x_velocity = 0 

            
        # Dodajemy objekty 
        add_object += 1
        if add_object == object_limit:
            x_range = [50,150,250,350,450,550,650,750]
            collect_limit += 1
            #dodajemy 2 przeszkody 
            x1_position = random.choice(x_range)
            x_range.remove(x1_position)
            asteroids_Sprite.add(Asteroid(potato_head_file, x1_position, speed))
            x2_position = random.choice(x_range)
            x_range.remove(x2_position)
            asteroids_Sprite.add(Asteroid(asteroid_file, x2_position, speed))
            if collect_limit == 1:
                x_position = random.choice(x_range)
                asteroid_type = random.choice([asteroid_file, potato_head_file])
                asteroids_Sprite.add(Asteroid(asteroid_type, x_position, speed))
            if collect_limit == 2: #w co drugin rzędzie dodajemy 1 pickle Ricka
                x_position = random.choice(x_range)
                collect_Sprite.add(CollectItem(x_position,speed))
                collect_limit = 0
            add_object = 0
            
                    
        #Aktualizuj wszystkie sprite'y         
        ship_Sprite.update()
        asteroids_Sprite.update()  
        collect_Sprite.update()
        
        #Wyczyść ekran
        ship_Sprite.clear(screen, background)
        asteroids_Sprite.clear(screen, background)   
        collect_Sprite.clear(screen, background)
        score_Sprite.clear(screen, background)
        lives_Sprire.clear(screen, background)
        
        #Rysuj sprite'y na ekranie
        ship_Sprite.draw(screen)
        asteroids_Sprite.draw(screen)
        collect_Sprite.draw(screen)
        score_Sprite.draw(screen)
        lives_Sprire.draw(screen) 
        
        # Sprawdzamy ile Pikle Rików zebrano
        for hit in pygame.sprite.groupcollide(ship_Sprite,collect_Sprite,False, True):
            wubba_sound.play()
            score += 1
            score_Sprite.update()
            
        # Sprawdzamy czy uderzono w asteroide
        for hit in pygame.sprite.groupcollide(asteroids_Sprite,ship_Sprite,True, False):
            boom_sound.play()
            lives += -1
            lives_Sprire.update()
            ship.explosion()
            time.sleep(0.2)
            screen.fill(black)
            ship_Sprite.draw(screen)
            asteroids_Sprite.draw(screen)
            collect_Sprite.draw(screen)
            score_Sprite.draw(screen)
            lives_Sprire.draw(screen) 
            
            if lives == 0:
                display_text("Game Over", 120, y_pos = window_height*0.4)
                display_text(f"Score: {score}", 120, y_pos = window_height*0.6)
                save_best_score(score)
                pygame.display.update()
                time.sleep(2.5)
                running = False
                # main_loop()
            
            
        pygame.display.update()
        
game_intro()    
    

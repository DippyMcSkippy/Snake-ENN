import turtle
import time
import random


class SnakeGame:
    def __init__(self):

        # Initialize constants
        self.width = 600 #due to constrain with NEAT you cannot chage tehvalues of the size
        self.height = 600
        self.grid_width = int((self.width / 2) - 40)
        self.grid_height = int((self.height / 2) - 40)
        self.bomb_num = ((self.grid_width * 2) // 40) * ((self.grid_height * 2) // 40) // 5
        self.score = 0
        self.high_score = 0
        self.delay = 0
        self.bombs = []
        self.segments = []
        self.can_move = True
        self.pending_segment = False
        self.last_tail_position = (0, 0)
        self.positions = []
        self.start_time = time.time()  # Track the start time
        self.max_time = 60  # Time limit in seconds (e.g., 60 seconds)
        self.max_same_action_count = 50  # Max allowed same actions in a row
        self.same_action_count = 0  # Counter for consecutive same actions
        self.last_action = None  # Store the last action


        # Setup screen
        self.wn = turtle.Screen()
        self.wn.title("Snake Game")
        self.wn.bgcolor("blue")
        self.wn.setup(width=self.width, height=self.height)
        self.wn.tracer(0)

        # Create game objects
        self.setup_game()

    def setup_game(self):


        self.wn.bgcolor("blue")
        self.wn.title("Snake Game")

        # Initialize game state
        self.score = 0
        self.high_score = 0
        self.bombs.clear()  # Remove any previous bombs
        self.segments.clear()  # Remove any previous snake segments

        # Create game objects
        self.head = self.create_head()
        self.food = self.create_food()
        self.pen = self.create_score_pen()

        # Setup bombs again
        self.setup_bombs()

        # Spawn food
        self.food_spawn(self.food)

        self.update_score()  # Update score display

    def calculate_num_inputs(self):
        return 1714

    def get_state(self):
        # Base state info (normalized)
        state = [
            self.head.xcor() / self.grid_width,
            self.head.ycor() / self.grid_height,
            self.grid_width,
            self.grid_height,
            # Convert bomb coordinates to list
            [tuple(bomb.pos()) for bomb in self.bombs],
            # Convert segment coordinates to list
            [tuple(segment.pos()) for segment in self.segments]
        ]
        fixed_inputs = list(state[:4])
        max_bombs = 175
        max_segments = 680


        bomb_positions = []
        for bomb in state[4][:max_bombs]:  # Limit to max_bombs
            bomb_positions.append(bomb[0])  # Add x coordinate
            bomb_positions.append(bomb[1])  # Add y coordinate
        while len(bomb_positions) < max_bombs * 2:  # Each bomb has two values (x, y)
            bomb_positions.extend([0, 0])

        segment_positions = []
        for segment in state[5][:max_segments]:  # Limit to max_segments
            segment_positions.append(segment[0])  # Add x coordinate
            segment_positions.append(segment[1])  # Add y coordinate
        while len(segment_positions) < max_segments * 2:  # Each segment has two values (x, y)
            segment_positions.extend([0, 0])

        flattened_state = fixed_inputs + bomb_positions + segment_positions

        return flattened_state

    def is_direction_dangerous(self, direction):
        """Check if moving in a direction would result in death"""
        future_x = self.head.xcor()
        future_y = self.head.ycor()

        if direction == "up":
            future_y += 20
        elif direction == "down":
            future_y -= 20
        elif direction == "left":
            future_x -= 20
        elif direction == "right":
            future_x += 20

        # Check bombs
        for bomb in self.bombs:
            if abs(bomb.xcor() - future_x) < 20 and abs(bomb.ycor() - future_y) < 20:
                return True

        # Check segments
        for segment in self.segments:
            if abs(segment.xcor() - future_x) < 20 and abs(segment.ycor() - future_y) < 20:
                return True

        return False

    def get_right_direction(self):
        """Get direction if turning right"""
        directions = {"up": "right", "right": "down", "down": "left", "left": "up"}
        return directions.get(self.head.direction, "right")

    def get_left_direction(self):
        """Get direction if turning left"""
        directions = {"up": "left", "left": "down", "down": "right", "right": "up"}
        return directions.get(self.head.direction, "left")

    def step(self, action):
        """Execute one game step based on AI action"""
        current_time = time.time()  # Get the current time
        elapsed_time = current_time - self.start_time  # Calculate elapsed time


        # Calculate reward
        reward = 0
        done = False

            # Convert network output to direction


        if action == self.last_action:
            self.same_action_count += 1
        else:
            self.same_action_count = 0
            reward += 0.1

        if self.same_action_count >= self.max_same_action_count:
            #print("Same action chosen too many times, ending the game!")

            self.same_action_count = 0  # reste count so it can gothat direction on spawn
            self.game_over()
            reward -= 5 #penlize
            done = True

            return reward, done, self.score  # Return penalty and end the game

        self.last_action = action


        if action == 0:  # Up
            self.go_up()

        elif action == 1:  # Down
            self.go_down()

        elif action == 2:  # Left
            self.go_left()

        elif action == 3:  # Right
            self.go_right()

        # Force move regardless of direction
        #self.move()
        self.update()

        # Check collisions
        if self.check_collision():
            reward -= 1
            self.game_over()
            done = True
        elif self.head.distance(self.food) < 20:
            reward += 10


        return reward, done, self.score

    def create_head(self):
        head = turtle.Turtle()
        head.shapesize(stretch_wid=1, stretch_len=1)
        head.shape("square")
        head.color("white")
        head.penup()
        head.goto(0, 0)
        head.direction = "Stop"
        return head

    def create_food(self):
        food = turtle.Turtle()
        food.shapesize(stretch_wid=1, stretch_len=1)
        food.shape("circle")
        food.color("red")
        food.penup()
        food.speed(0)
        self.food_spawn(food)
        return food

    def create_score_pen(self):
        pen = turtle.Turtle()
        pen.speed(0)
        pen.shape("square")
        pen.color("white")
        pen.penup()
        pen.hideturtle()
        pen.goto(0, (self.grid_height) - 20)
        pen.write("Score : 0  High Score : 0", align="center", font=("candara", 24, "bold"))
        return pen

    def food_spawn(self, food):
        x = random.randint(-self.grid_width // 20, self.grid_width // 20) * 20
        y = random.randint(-self.grid_height // 20, self.grid_height // 20) * 20
        for bomb in self.bombs:
            if x == bomb.xcor() and y == bomb.ycor():
                x = (x + 20) % self.grid_width
        for segment in self.segments:
            if x == segment.xcor() and y == segment.ycor():
                x = (x + 20) % self.grid_width
        food.goto(x, y)

    def setup_bombs(self):
        for _ in range(self.bomb_num):
            bomb = turtle.Turtle()
            bomb.shapesize(stretch_wid=1, stretch_len=1)
            bomb.shape("square")
            bomb.color("black")
            bomb.speed(0)
            bomb.penup()
            self.bomb_spawn(bomb)
            self.bombs.append(bomb)

    def bomb_spawn(self, bomb):
        x = random.randint(-self.grid_width // 20, self.grid_width // 20) * 20
        y = random.randint(-self.grid_height // 20, self.grid_height // 20) * 20
        for existing_bomb in self.bombs:
            if x == existing_bomb.xcor() and y == existing_bomb.ycor():
                x = (x + 20) % self.grid_width
        bomb.goto(x, y)

    def reset_game(self):
        #print("Resetting game...")

        for bomb in self.bombs:

            bomb.hideturtle()
        self.bombs.clear()

        for segment in self.segments:

            segment.hideturtle()
        self.segments.clear()

        self.head.direction = "Stop"
        self.head.goto(0, 0)
        self.score = 0
        #print("Score reset to 0.")

        self.update_score()
        self.setup_bombs()
        self.food_spawn(self.food)
        self.same_action_count = 0

    def update_score(self):
        self.pen.clear()
        self.pen.write(f"Score : {self.score} High Score : {self.high_score}",
                       align="center", font=("candara", 24, "bold"))

    def go_up(self):
        if self.can_move and self.head.direction != "down":
            self.head.direction = "up"
            self.can_move = False

    def go_down(self):
        if self.can_move and self.head.direction != "up":
            self.head.direction = "down"
            self.can_move = False

    def go_left(self):
        if self.can_move and self.head.direction != "right":
            self.head.direction = "left"
            self.can_move = False

    def go_right(self):
        if self.can_move and self.head.direction != "left":
            self.head.direction = "right"
            self.can_move = False

    def move(self):
        if self.head.direction == "up":
            self.head.sety(self.head.ycor() + 20)
        elif self.head.direction == "down":
            self.head.sety(self.head.ycor() - 20)
        elif self.head.direction == "left":
            self.head.setx(self.head.xcor() - 20)
        elif self.head.direction == "right":
            self.head.setx(self.head.xcor() + 20)
        self.can_move = True

    def check_collision(self):
        # Check bomb collisions
        for bomb in self.bombs:
            if bomb.distance(self.head) < 20:
                #print("Death by bomb")
                return True

        # Check segment collisions
        for segment in self.segments:
            if segment.distance(self.head) < 20:
                print(f"Death by segment")
                #print(f"Head: ({self.head.xcor()}, {self.head.ycor()})")
                #print(f"Positions list: {self.positions}")
                #print(f"Segment positions: {[(s.xcor(), s.ycor()) for s in self.segments]}")
                return True

        return False

    def update(self):
        self.wn.update()

        # 1. Store old head position
        old_head_x = self.head.xcor()
        old_head_y = self.head.ycor()

        # 2. Move head
        self.move()

        # 3. Handle portal walls
        if self.head.xcor() > self.grid_width + 20:
            self.head.goto(-self.grid_width - 20, self.head.ycor())
        if self.head.xcor() < -self.grid_width - 20:
            self.head.goto(self.grid_width + 20, self.head.ycor())
        if self.head.ycor() > self.grid_height + 20:
            self.head.goto(self.head.xcor(), -self.grid_height - 20)
        if self.head.ycor() < -self.grid_height - 20:
            self.head.goto(self.head.xcor(), self.grid_height + 20)

        # 4. Move segments
        for index in range(len(self.segments) - 1, 0, -1):
            x = self.segments[index - 1].xcor()
            y = self.segments[index - 1].ycor()
            self.segments[index].goto(x, y)
        if len(self.segments) > 0:
            self.segments[0].goto(old_head_x, old_head_y)

        # 5. Check collisions
        if self.check_collision():
            self.game_over()
            return

        # 6. Handle food
        if self.head.distance(self.food) < 20:
            new_segment = turtle.Turtle()
            new_segment.speed(0)
            new_segment.shape("square")
            new_segment.color("orange")
            new_segment.penup()
            if len(self.segments) > 0:
                new_segment.goto(self.segments[-1].xcor(), self.segments[-1].ycor())
            else:
                new_segment.goto(old_head_x, old_head_y)
            self.segments.append(new_segment)

            self.score += 10
            if self.score > self.high_score:
                self.high_score = self.score
            self.update_score()
            self.food_spawn(self.food)

    def grow_snake(self):
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("orange")
        new_segment.penup()

        # Get the position of the last segment or head
        if len(self.segments) == 0:
            last_x = self.head.xcor()
            last_y = self.head.ycor()
        else:
            last_x = self.segments[-1].xcor()
            last_y = self.segments[-1].ycor()

        # Place new segment one unit behind in the current direction
        if self.head.direction == "up":
            new_segment.goto(last_x, last_y - 20)
        elif self.head.direction == "down":
            new_segment.goto(last_x, last_y + 20)
        elif self.head.direction == "left":
            new_segment.goto(last_x + 20, last_y)
        elif self.head.direction == "right":
            new_segment.goto(last_x - 20, last_y)

        self.segments.append(new_segment)


    def game_over(self):
        self.pen.clear()
        self.pen.write(f"Game Over! Final Score: {self.score}",
                       align="center", font=("candara", 24, "bold"))

        self.reset_game()

    def run_game(self):
        while True:
            self.update()





if __name__ == "__main__":
    game = SnakeGame()
    game.wn.listen()
    game.wn.onkeypress(game.go_up, "w")
    game.wn.onkeypress(game.go_down, "s")
    game.wn.onkeypress(game.go_left, "a")
    game.wn.onkeypress(game.go_right, "d")
    game.run_game()

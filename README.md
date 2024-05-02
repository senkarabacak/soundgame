# Forest Hamsters Game

Forest Hamsters is a simple game where you play as a hamster tasked with restoring peace to a forest by capturing disruptive birds.

## How to Play

- Use the arrow keys to navigate the hamster.
- Press 'n' when you hear a bird sound to capture it.
- You must find matching bird sounds and capture both to remove them from the forest.
- Avoid collisions with the forest's borders.

## Levels

- **Tutorial**: Learn the game mechanics and controls.
- **Level 1**: Capture birds in the first level.
- **Level 2**: More challenging with additional birds to capture.
- **Level 3**: The final level with the most birds to capture.

## Controls

- **Arrow Keys**: Move the hamster.
- **'n' Key**: Capture a bird.
- **'h' Key**: Toggle hamster visibility.
- **'g' Key**: Toggle bird visibility.


## Web Deploy

the game is deployed continuously into the itchi.io and can be played under https://dnzsnkrbck.itch.io/ninjahamster
(password is in the itchio_pass file)


## Installation


1. Clone the repository:

`git clone https://github.com/senkarabacak/soundgame.git`

2. Install dependencies:

install renpy and change to directory

`wget https://www.renpy.org/dl/8.2.1/renpy-8.2.1-sdk.tar.bz2`

`tar -jxvf renpy-8.2.1-sdk.tar.bz2`

`cd renpy-8.2.1-sdk`

install python libraries 

`pip install -r requirements.txt`

3. Build the game:

`cd renpy-8.2.1-sdk`

`./renpy.sh launcher distribute /path/to/soundgame --destination path/to/output_build`

Example: `./renpy.sh launcher distribute ../soundgame --destination ../output_build`

4. Run game:

After successfully building the game, navigate to the output_build folder. Inside, you'll find the built version of the game for your operating system.

Unzip the appropriate OS distribution file, for example, "ninja_hamster.zip". Then, simply run the game by clicking on the game symbol or executable file.







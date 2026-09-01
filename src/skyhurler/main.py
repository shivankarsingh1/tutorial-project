
'''lets game be launched from command line and sets up the game context and scenes'''
import argparse


'''game imported inside main()'''
def main():
    parser = argparse.ArgumentParser(prog="skyhurler")
    parser.add_argument(
        "--fullscreen",
        action="store_true",
        help="run the game in fullscreen mode (default is windowed)",
    )
    args = parser.parse_args()

    from skyhurler.core.game import Game

    game = Game(fullscreen=args.fullscreen)
    game.run()


'''makes sure that game only starts if this file is run directly'''
if __name__ == "__main__":
    main()

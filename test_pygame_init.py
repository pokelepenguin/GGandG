import pygame


def main():
    try:
        print("Initializing Pygame")
        pygame.init()
        print("Pygame initialized")

        print("Setting up the display mode")
        screen = pygame.display.set_mode((1920, 1080))
        print("Display mode set")

        pygame.display.set_caption('Pygame Test')
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        pygame.quit()
        print("Pygame closed successfully")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()

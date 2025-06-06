import os
import pygame
from palette import load_palette
from tree import Tree

def button(w, h, text):
	button_rect = pygame.Surface((w, h), pygame.SRCALPHA)
	pygame.draw.rect(button_rect, (255, 255, 255), (0, 0, w, h), 0, 8)
	pygame.draw.rect(button_rect, (55, 55, 55), (0, 0, w, h), 4, 8)

	font = pygame.font.Font('freesansbold.ttf', 16)
	text = font.render(text, True, (55, 55, 55))
	textRect = text.get_rect()
	textRect.center = (w // 2, h // 2 + 2)
	button_rect.blit(text, textRect)

	return button_rect


pygame.init()
window = pygame.display.set_mode((400, 600))
palette = load_palette("custom0")
tree = Tree(palette, 50)
new_tree_button_surf = button(100, 50, "New Tree")
new_tree_button_rect = pygame.Rect(20, 20, 100, 50)
save_button_surf = button(100, 50, "Save")
save_button_rect = pygame.Rect(140, 20, 100, 50)


while True:
	tree.grow()
	window.fill((130, 170, 70)) # Background Color (On Preview)
	tree.draw(window, (0, 0))
	window.blit(new_tree_button_surf, new_tree_button_rect)
	window.blit(save_button_surf, save_button_rect)
	pygame.display.flip()


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit()
		elif (event.type == pygame.MOUSEBUTTONDOWN):
			if new_tree_button_rect.collidepoint(event.pos):
				tree = Tree(palette, 50)
				print("generating new tree")
			elif save_button_rect.collidepoint(event.pos):
				image = pygame.Surface(tree.rect.size, pygame.SRCALPHA)
				# image.fill((130, 170, 70, 255)) # Background Color (On Export)
				image.blit(tree.surface, (0, 0))

				# Export the as tree.png
				i = 0
				while True:
					filename = f"tree_{i}.png"
					if not os.path.exists(filename):
						pygame.image.save(image, filename)
						print(f"Image saved as: {filename}")
						break
					i += 1



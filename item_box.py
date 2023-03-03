import pygame
from damagetext import DamageText
class ItemBox(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y, TILE_SIZE):
        pygame.sprite.Sprite.__init__(self)
        # pick up boxes
        self.health_box_img = pygame.image.load("assets/img/icons/health_box.png").convert_alpha()
        self.damage_box_img = pygame.image.load("assets/img/icons/damage_box.png").convert_alpha()
        self.ammo_box_img = pygame.image.load("assets/img/icons/ammo_box.png").convert_alpha()
        self.item_boxes = {
    "Health": self.health_box_img,
    "Damage": self.damage_box_img,
    "Ammo": self.ammo_box_img
}
        self.item_type = item_type
        self.image = self.item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self, player, screen_scroll, damage_text_group):
        # scroll
        self.rect.x += screen_scroll
        # check if the player has picked up the box
        if pygame.sprite.collide_rect(self, player):
            # check what kind of box it was
            if self.item_type == "Health":
                player.health += 25
                if player.health > player.max_health:
                    player.health = player.max_health
                damage_text = DamageText(player.rect.centerx, player.rect.y, "25", (0, 255, 0))
                damage_text_group.add(damage_text)
            elif self.item_type == "Damage":
                player.attack_damage += 25
                player.projectile_damage += 25
            elif self.item_type == "Ammo":
                player.ammo += 5
            # delete the item box
            self.kill()
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader
from ursina.prefabs.health_bar import HealthBar
from ursina.prefabs.particlesystem import ParticleSystem
import random

# -------------------------
# Pure Python Paper Mario Vibes Demo
# -------------------------

app = Ursina()
window.title = 'Paper Mario RPG - Pure Python Vibes'
window.size = (600, 400)
window.borderless = False
window.color = color.rgb(150, 200, 255)

# Environment
scene.fog_color = window.color
scene.fog_density = 0.02
Sky()

# Lighting
directional_light = DirectionalLight(shadows=True)
directional_light.color = color.rgba(255,255,255,200)
directional_light.rotation = Vec3(45, -45, 0)
AmbientLight(color=color.rgb(100,100,120))

# Audio (place your file at 'assets/music/theme.mp3')
theme = Audio('assets/music/theme.mp3', loop=True, autoplay=True)

# UI Elements
health_bar = HealthBar()
dialogue_text = Text('', parent=camera.ui, origin=(0,0), position=(0,-0.4), scale=1.2, background=True)

def show_dialogue(message, duration=3):
    dialogue_text.text = message
    invoke(lambda: setattr(dialogue_text, 'text', ''), delay=duration)

# Particles
sparkles = ParticleSystem(parent=scene, texture='circle', color=color.white,
                            emission_rate=30, lifetime=2, velocity=Vec3(0,1,0),
                            scale=0.1)

# Camera & Controls
player_controller = FirstPersonController(y=1)
camera.shader = lit_with_shadows_shader

# Paper-style Block Entity
def create_paper_block(position):
    block = Entity(model='cube', color=color.white, scale=(1,1,0.1), position=position, collider='box')
    Entity(parent=block, model='cube', color=color.black, scale=Vec3(1.05,1.05,0.11), position=(0,0,-0.01))
    return block

blocks = [create_paper_block((x,0,z)) for x in range(-3,4,2) for z in range(-3,4,2)]

def shake_camera(duration=0.5, magnitude=0.2):
    original_pos = camera.position
    def shake():
        camera.position = original_pos + Vec3(
            random.uniform(-magnitude, magnitude),
            random.uniform(-magnitude, magnitude),
            random.uniform(-magnitude, magnitude)
        )
    # schedule shakes
    for i in range(int(duration / 0.03)):
        invoke(shake, delay=i * 0.03)
    invoke(lambda: setattr(camera, 'position', original_pos), delay=duration)

# Input Handling
def input(key):
    if key == 'enter':
        show_dialogue('A wild Goomba appeared!', duration=4)
        shake_camera()

# Main Loop
def update():
    # could update particles or other logic here
    pass

if __name__ == '__main__':
    app.run()

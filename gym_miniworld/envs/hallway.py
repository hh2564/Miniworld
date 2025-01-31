import math

from gymnasium import spaces

from gym_miniworld.entity import Box
from gym_miniworld.miniworld import MiniWorldEnv


class Hallway(MiniWorldEnv):
    """
    ## Description

    Environment in which the goal is to go to a red box
    at the end of a hallway

    ## Action Space

    | Num | Action                      |
    |-----|-----------------------------|
    | 0   | turn left                   |
    | 1   | turn right                  |
    | 2   | move forward                |

    ## Observation Space

    The observation space is an `ndarray` with shape `(obs_height, obs_width, 3)`
    representing the view the agents sees.

    ## Rewards:

    +(1 - 0.2 * (step_count / max_episode_steps)) when red box reached

    ## Arguments

    ```python
    FourRooms(length=12)
    ```

    `length`: length of the entire space

    """

    def __init__(self, length=12, **kwargs):
        assert length >= 2
        self.length = length

        super().__init__(max_episode_steps=250, **kwargs)

        # Allow only movement actions (left/right/forward)
        self.action_space = spaces.Discrete(self.actions.move_forward + 1)

    def _gen_world(self):
        # Create a long rectangular room
        room = self.add_rect_room(min_x=-1, max_x=-1 + self.length, min_z=-2, max_z=2)

        # Place the box at the end of the hallway
        self.box = self.place_entity(Box(color="red"), min_x=room.max_x - 2)

        # Place the agent a random distance away from the goal
        self.place_agent(
            dir=self.np_random.uniform(-math.pi / 4, math.pi / 4), max_x=room.max_x - 2
        )

    def step(self, action):
        obs, reward, termination, truncation, info = super().step(action)

        if self.near(self.box):
            reward += self._reward()
            termination = True

        return obs, reward, termination, truncation, info

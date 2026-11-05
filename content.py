"""Everything the three Liberty Park pages say, and how each one is colored.

Edit this file, then run `python build.py`. Never edit option-N/index.html by
hand: build.py overwrites it.

Captions describe only what the renders show. They name no products and make
no compliance claims; add those here if and when the owner supplies them.
"""

# Where the pages are served from. The QR codes encode SITE + "/option-N/".
SITE = "https://jdietz18.github.io/Liberty-Park"

PARK = "Liberty Park"

# Shown in every footer.
DISCLAIMER = (
    "Renderings show design intent. Colors, equipment and site details may "
    "change before construction."
)

# True adds links to the other two options in each footer (owner's choice,
# 2026-11-05). Set False to make each page stand alone again.
CROSS_LINKS = True

# The plan-view render (03) is the same camera in all three options. These
# place the circle inside that picture: its center as a fraction of the image
# width and height. The wheel is cropped to the full image height.
PLAN_CENTER_X = 0.503
PLAN_CENTER_Y = 0.500

OPTIONS = {
    1: {
        "headline": "Bright from every side.",
        "lede": (
            "Option 1 sets twin towers, a net climber and a long run of swings "
            "around the center tree, in teal, berry and violet over "
            "sand-colored surfacing."
        ),
        "colors": {
            "bg": "#1E1A4D",      # deep violet, from the shade canopy
            "panel": "#28236A",
            "ink": "#F6E8BE",     # the sand-colored surfacing
            "muted": "#C9BFA9",
            "a1": "#E0356F",      # berry posts
            "a2": "#2CC0B7",      # teal roofs and slides
            "a3": "#B9A2F2",      # lilac slide
            "on_a1": "#FFFFFF",
            "scrim": "18, 14, 52",
        },
        "words": ["Climb", "Slide", "Swing", "Spin", "Balance"],
        "hero": [1, 9, 4],
        "plan": 3,
        "zones": [
            ("Towers and net",
             "The widest area holds the twin-tower structure and the rope net "
             "climber, with open ground between them."),
            ("Swings",
             "A long run of swing bays fills its own area, with a group ride "
             "set in front."),
            ("Shaded deck",
             "The lower, ramped structure sits under a violet canopy, with "
             "spinners close by."),
        ],
        "walk": [1, 4, 8, 2, 5, 6, 7],
        "above": [
            (9, "From above",
             "The towers anchor one side of the circle. Paths meet at the tree "
             "in the middle."),
            (10, "The other way round",
             "Swings in front, the shaded deck to the right, the towers beyond."),
        ],
        "views": {
            1: ("The towers",
                "Two towers joined by an enclosed bridge, with tube slides "
                "curling down either side."),
            2: ("Shaded deck and spinners",
                "A ramped deck with play panels under a violet canopy. "
                "Spinners sit in the open beside it."),
            3: ("Plan view", "The whole circle from directly above."),
            4: ("Ramp side of the towers",
                "Play panels line the ramp that leads onto the structure."),
            5: ("Double slide",
                "The lower structure has a side-by-side slide and its own shade."),
            6: ("Net climber",
                "A rope net rises to a single mast, with seating behind it."),
            7: ("Swings",
                "One long run of swing bays, with a group ride set in front."),
            8: ("Tower close up",
                "A climbing wall, a curved ladder and a slide meet at the "
                "taller tower."),
            9: ("Aerial, towers in front",
                "The towers anchor one side of the circle."),
            10: ("Aerial, swings in front",
                 "Swings in front, the shaded deck to the right."),
        },
    },
    2: {
        "headline": "Blue ground, deep shade.",
        "lede": (
            "Option 2 puts shade first: navy canopies over the swings and the "
            "decks, wheat-colored posts, and blue surfacing across the whole "
            "circle."
        ),
        "colors": {
            "bg": "#EEF2F8",      # pale sky
            "panel": "#DDE5F2",
            "ink": "#131A55",     # navy shade fabric
            "muted": "#4A5486",
            "a1": "#2434A8",      # canopy blue
            "a2": "#C98F1E",      # wheat posts, deepened to read on a light page
            "a3": "#5E8F2F",      # leaf-green slides
            "on_a1": "#FFFFFF",
            "scrim": "12, 18, 62",
        },
        "words": ["Climb", "Slide", "Swing", "Spin", "Shade"],
        "hero": [1, 9, 2],
        "plan": 3,
        "zones": [
            ("Towers and dome",
             "The twin-tower structure shares the widest area with the dome "
             "climber, a spinner and balance pieces."),
            ("Shaded swings",
             "One long canopy covers the full run of swings. A smaller canopy "
             "stands beside it."),
            ("Shaded deck",
             "The lower, ramped structure sits under two navy canopies."),
        ],
        "walk": [1, 4, 8, 2, 5, 6, 7],
        "above": [
            (9, "From above",
             "Navy canopies mark the shaded spots. Paths meet at the tree in "
             "the middle."),
            (10, "The other way round",
             "The long swing canopy in front, the towers beyond."),
        ],
        "views": {
            1: ("The towers",
                "Two towers and an enclosed bridge in wheat and navy, with "
                "tube slides on both sides."),
            2: ("Shaded deck",
                "A ramped deck under two navy canopies, with play panels along "
                "the rail and stepping pods in front."),
            3: ("Plan view", "The whole circle from directly above."),
            4: ("Ramp side of the towers",
                "Play panels, a crawl tunnel and chimes at ground level, "
                "below the bridge."),
            5: ("Slides and shade",
                "The lower structure, with slides at each end and canopies "
                "overhead."),
            6: ("Dome climber",
                "A rope net strung inside a frame of angled poles."),
            7: ("Shaded swings",
                "A long canopy covers the full run of swings."),
            8: ("Tower close up",
                "Curved posts, climbers and a slide gather at the taller tower."),
            9: ("Aerial, towers in front",
                "Navy canopies mark the shaded spots."),
            10: ("Aerial, shade in front",
                 "The long swing canopy in front, the towers beyond."),
        },
    },
    3: {
        "headline": "A forest in the round.",
        "lede": (
            "Option 3 turns the circle into a forest: cabin roofs, pine-tree "
            "posts and stump climbers on green surfacing, with wide shade "
            "sails over the swings and the track ride."
        ),
        "colors": {
            "bg": "#12382C",      # pine
            "panel": "#1A4A3A",
            "ink": "#F2EDDC",     # shade-sail canvas
            "muted": "#BFCBB8",
            "a1": "#E57B2E",      # orange posts
            "a2": "#DCD25E",      # yellow pine toppers
            "a3": "#49BE95",      # green canopies
            "on_a1": "#1A1208",
            "scrim": "10, 30, 22",
        },
        "words": ["Climb", "Slide", "Swing", "Glide", "Explore"],
        "hero": [1, 9, 4],
        "plan": 3,
        "zones": [
            ("Forest structure",
             "Cabin towers, pine-tree posts and a rock climber fill the widest "
             "area, with swings under a sail along the path."),
            ("Smaller structure",
             "Play panels, a cabin and mushroom steppers under two green "
             "canopies."),
            ("Track ride",
             "Two overhead tracks run side by side under a pair of shade sails."),
        ],
        "walk": [1, 4, 6, 5, 2, 7, 8, 11, 12],
        "above": [
            (9, "From above",
             "The forest structure fills one side. Paths meet at the tree in "
             "the middle."),
            (13, "Under the sails",
             "Three shade sails cover the track ride and the swings."),
        ],
        "views": {
            1: ("The forest structure",
                "Cabin roofs and pine-tree posts, with a rock climber in the "
                "middle and slides at either end."),
            2: ("Smaller structure",
                "Play panels, a cabin and a slide under two green canopies."),
            3: ("Plan view", "The whole circle from directly above."),
            4: ("Slide through the stump",
                "A slide drops out of a tree stump below the cabin tower."),
            5: ("Mushroom steppers",
                "Steppers, climbers and a slide along the edge of the smaller "
                "structure."),
            6: ("Ramp onto the deck",
                "A ramp leads from the ground onto the structure."),
            7: ("Play panels and chimes",
                "Panels to spin, match and play music, at ground level."),
            8: ("Track ride",
                "Two overhead tracks run side by side beneath the shade sails."),
            9: ("Aerial, forest structure in front",
                "The forest structure fills one side of the circle."),
            10: ("Aerial, sails and canopies",
                 "Shade sails on one side, green canopies on the other."),
            11: ("Track ride seats",
                 "One of the two tracks carries a molded, high-backed seat."),
            12: ("Shaded swings", "A row of swings under one long sail."),
            13: ("Aerial, shade sails in front",
                 "Three shade sails cover the track ride and the swings."),
            14: ("Aerial, the forest structure",
                 "The forest structure from above, with ramps linking its decks."),
        },
    },
}

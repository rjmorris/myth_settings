import dataset
from dotenv import find_dotenv
from dotenv import load_dotenv
import os
from pprint import pprint

from settings import JumpPoints


load_dotenv(find_dotenv())
db = dataset.connect(os.environ['DB_URI'])

#---------------------------------------------------------------------------
# This example demonstrates comparing and updating keybindings for jump
# points. The workflow is similar for settings and generic keybindings.

j = JumpPoints(db)

# Display the hosts stored in the database.
pprint(j.hosts)

# Suppose two of the hosts are named 'ned' and 'moe'. Get lists containing
# the keybindings they have in common and where they differ.
only_ned, only_moe, same, different = j.compare(
    host1 = 'ned',
    host2 = 'moe',
)

# Inspect the keybindings assigned in ned but not moe.
pprint(only_ned)

# Inspect the keybindings assigned in both but to different keys.
pprint(different)

# After inspecting the keybinding differences, suppose we want to update
# moe's in all cases where they differ from ned's. Copy them over with the
# following. (Commented out to avoid running this accidentally, since it
# modifies the database.)
# j.copy(
#     from_host = 'ned',
#     to_host = 'moe',
#     copy_dests = [d[0] for d in different]
# )

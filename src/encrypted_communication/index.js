const {USERS, IPFS_BASE_URI, shares} = require("./constants")
const messenger = require("./messenger")

// messenger.black_hole_communication(USERS.USER1, USERS.USER2, "TEST MESSAGE")

// messenger.user_to_user_communication(USERS.USER1, USERS.USER2, "TEST MESSAGE")

const token_uri = IPFS_BASE_URI + shares.share_1_CID
messenger.nft_communication(USERS.USER1, USERS.USER2, token_uri)

console.log("END")
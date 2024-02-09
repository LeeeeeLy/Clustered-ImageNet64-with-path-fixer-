import os
import shutil
from random import sample

# Dictionary of ImageNet labels from https://gist.github.com/aaronpolhamus/964a4411c0906315deb9f4a3723aac57
imagenet_labels = {
"n07565083": "menu", "n07831146": "carbonara", "n09229709": "bubble", "n07695742": "pretzel", "n06794110": "street sign", "n15075141": "toilet tissue", "n07684084": "French loaf", "n06874185": "traffic light", "n07693725": "bun", "n07836838": "sauce", "n07583066": "dip", "n07802026": "hay", "n07697537": "hotdog", "n07697313": "hamburger", "n07711569": "mashed potato", "n07860988": "dough", "n07590611": "stew", "n07871810": "meat loaf", "n07584110": "soup", "n07875152": "potpie", "n07880968": "burrito", "n07873807": "pizza", "n07579787": "plate", "n07615774": "dessert", "n07614500": "dessert", "n07613480": "dessert", "n09246464": "cliff", "n09468604": "valley", "n09193705": "natural elevation", "n09472597": "natural elevation", "n09399592": "natural elevation", "n09421951": "natural elevation", "n09256479": "coral reef", "n09332890": "shore", "n09428293": "shore", "n09288635": "geyser", "n07920052": "coffee", "n07892512": "wine", "n07932039": "mixed drink", "n07930864": "cup", "n07720875": "pepper", "n07714571": "cabbage", "n07714990": "broccoli", "n07715103": "cauliflower", "n07717410": "squash", "n07717556": "squash", "n07716358": "squash", "n07716906": "squash", "n07718472": "cucumber", "n07718747": "vegetable", "n07730033": "vegetable", "n07734744": "mushroom", "n07742313": "apple", "n07745940": "strawberry", "n07747607": "orange", "n07749582": "lemon", "n07753113": "fruit", "n07753275": "pineapple", "n07753592": "banana", "n07754684": "fruit", "n07760859": "fruit", "n07768694": "fruit", "n12267677": "fruit", "n12620546": "fruit", "n13133613": "corn", "n11879895": "rapeseed", "n12144580": "corn", "n12768682": "fruit", "n03452741": "piano", "n04515003": "piano", "n03017168": "chime", "n03249569": "drum", "n03447721": "percussion instrument", "n03720891": "percussion instrument", "n03721384": "percussion instrument", "n04311174": "drum", "n02787622": "stringed instrument", "n02992211": "stringed instrument", "n04536866": "stringed instrument", "n03495258": "stringed instrument", "n02676566": "stringed instrument", "n03272010": "stringed instrument", "n03854065": "organ", "n03110669": "brass", "n03394916": "brass", "n04487394": "brass", "n02672831": "accordion", "n03494278": "wind instrument", "n03840681": "wind instrument", "n03884397": "wind instrument", "n02804610": "wind instrument", "n03838899": "wind instrument", "n04141076": "wind instrument", "n03372029": "wind instrument", "n04592741": "wing", "n03868863": "mask", "n04251144": "snorkel", "n03691459": "speaker", "n03759954": "microphone", "n04152593": "screen", "n03793489": "mouse", "n03271574": "fan", "n03843555": "filter", "n04332243": "filter", "n04265275": "heater", "n04330267": "stove", "n03467068": "guillotine", "n02794156": "measuring instrument", "n04118776": "rule", "n03841143": "measuring instrument", "n04141975": "measuring instrument", "n03197337": "watch", "n02708093": "clock", "n03196217": "clock", "n04548280": "clock", "n03544143": "hourglass", "n04355338": "measuring instrument", "n03891332": "measuring instrument", "n04328186": "measuring instrument", "n04317175": "stethoscope", "n04376876": "syringe", "n03706229": "compass", "n02841315": "binoculars", "n04009552": "projector", "n04356056": "sunglasses", "n03692522": "microscope", "n04044716": "radio telescope", "n03773504": "missile", "n02879718": "bow", "n02950826": "cannon", "n02749479": "gun", "n04086273": "gun", "n04090263": "gun", "n04008634": "weapon", "n03085013": "keyboard", "n04505470": "keyboard", "n03126707": "crane", "n03666591": "lighter", "n03995372": "tool", "n03000684": "tool", "n02666196": "tool", "n02977058": "machine", "n04238763": "ruler", "n03180011": "computer", "n03642806": "computer", "n03485407": "portable computer", "n03832673": "computer", "n06359193": "web site", "n03496892": "farm machine", "n04428191": "farm machine", "n04243546": "slot machine", "n04525305": "vending machine", "n03602883": "joystick", "n04372370": "switch", "n03532672": "mechanical device", "n02974003": "car", "n03874293": "wheel", "n03944341": "wheel", "n03992509": "wheel", "n03425413": "gas pump", "n02966193": "carousel", "n04371774": "swing", "n04067472": "reel", "n04040759": "radiator", "n03492542": "hard disc", "n04355933": "sunglass", "n03929660": "pick", "n02965783": "car mirror", "n04258138": "device", "n04074963": "remote control", "n03208938": "brake", "n02910353": "buckle", "n03476684": "clip", "n03627232": "knot", "n03075370": "lock", "n03874599": "lock", "n03804744": "nail", "n04127249": "pin", "n04153751": "screw", "n03803284": "muzzle", "n04162706": "seat belt", "n04228054": "ski", "n04579432": "whistle", "n02948072": "candle", "n03590841": "lamp", "n04286575": "lamp", "n04456115": "torch", "n03814639": "neck brace", "n03933933": "pier", "n04485082": "tripod", "n03733131": "maypole", "n03794056": "trap", "n04275548": "spider web", "n03498962": "ax", "n03041632": "knife", "n03658185": "knife", "n03954731": "tool", "n03649909": "garden tool", "n03481172": "hammer", "n03109150": "opener", "n02951585": "opener", "n03970156": "plunger", "n04154565": "tool", "n04208210": "shovel", "n03967562": "tool", "n03133878": "cooker", "n03400231": "pan", "n04596742": "pan", "n02939185": "pot", "n03063689": "pot", "n04398044": "pot", "n04270147": "turner", "n04367480": "cleaning implement", "n02906734": "cleaning implement", "n03876231": "brush", "n04116512": "eraser", "n03908714": "sharpener", "n03873416": "paddle", "n03976657": "rod", "n04033901": "pen", "n02783161": "pen", "n03388183": "pen", "n04277352": "spindle", "n03250847": "drumstick", "n03141823": "crutch", "n03355925": "flagpole", "n03729826": "matchstick", "n04264628": "keyboard", "n04039381": "racket", "n02835271": "bicycle", "n03792782": "bicycle", "n03393912": "vehicle", "n03895866": "vehicle", "n02797295": "handcart", "n04204347": "handcart", "n03791053": "motor scooter", "n03384352": "forklift", "n03272562": "locomotive", "n04310018": "locomotive", "n02704792": "vehicle", "n02701002": "car", "n02814533": "car", "n02930766": "cab", "n03100240": "car", "n03594945": "car", "n03670208": "car", "n03770679": "car", "n03777568": "car", "n04037443": "car", "n04285008": "car", "n03444034": "vehicle", "n03445924": "vehicle", "n03785016": "motor scooter", "n04252225": "vehicle", "n03345487": "fire engine", "n03417042": "truck", "n03930630": "truck", "n04461696": "truck", "n04467665": "truck", "n03796401": "van", "n03977966": "police van", "n04065272": "vehicle", "n04335435": "streetcar", "n03478589": "tank", "n04389033": "tank", "n04252077": "snowmobile", "n04465501": "tractor", "n04482393": "bicycle", "n04509417": "bicycle", "n03538406": "wagon", "n03599486": "wagon", "n03868242": "wagon", "n03482405": "basket", "n04204238": "basket", "n04423845": "thimble", "n03709823": "bag", "n02769748": "bag", "n04026417": "bag", "n04235860": "sleeping bag", "n03958227": "plastic bag", "n04597913": "spoon", "n03935335": "savings bank", "n03920288": "Petri dish", "n04263257": "bowl", "n03775546": "bowl", "n02747177": "bin", "n03062245": "shaker", "n04131690": "shaker", "n03991062": "pot", "n04553703": "basin", "n04493381": "tub", "n04522168": "vase", "n02815834": "container", "n02909870": "container", "n03786901": "mortar", "n02823428": "bottle", "n03983396": "bottle", "n04591713": "bottle", "n03937543": "bottle", "n04557648": "bottle", "n04579145": "bottle", "n04560804": "bottle", "n04562935": "water tower", "n04049303": "container", "n02808440": "bathtub", "n03633091": "ladle", "n02795169": "container", "n03950228": "container", "n03063599": "mug", "n03291819": "envelope", "n03764736": "can", "n02823750": "glass", "n03443371": "glass", "n02978881": "cassette", "n04476259": "tray", "n04254120": "soap dispenser", "n03871628": "package", "n02971356": "box", "n03014705": "chest", "n04125021": "safe", "n03908618": "pencil box", "n03127925": "box", "n03710193": "mailbox", "n03733805": "measuring cup", "n04548362": "wallet", "n02777292": "sports equipment", "n03535780": "horizontal bar", "n03888605": "horizontal bar", "n02790996": "weight", "n03255030": "weight", "n03982430": "pool table", "n06785654": "puzzle", "n03598930": "puzzle", "n04254680": "ball", "n03134739": "ball", "n03445777": "ball", "n02799071": "ball", "n03942813": "ball", "n04023962": "punching bag", "n04118538": "ball", "n02802426": "ball", "n04540053": "ball", "n04409515": "ball", "n03976467": "camera", "n04069434": "camera", "n02966687": "kit", "n03240683": "drilling platform", "n03584254": "iPod", "n03777754": "electronic equipment", "n03782006": "monitor", "n03857828": "electronic equipment", "n04004767": "printer", "n02979186": "electronic equipment", "n02992529": "telephone", "n03902125": "pay-phone", "n03187595": "telephone", "n04392985": "tape player", "n02988304": "electronic equipment", "n03924679": "photocopier", "n03888257": "parachute", "n04357314": "sunscreen", "n03916031": "perfume", "n03314780": "face powder", "n03676483": "lipstick", "n03690938": "lotion", "n03476991": "hair spray", "n02690373": "aircraft", "n04552348": "aircraft", "n02692877": "aircraft", "n02782093": "balloon", "n04266014": "space shuttle", "n03344393": "boat", "n03447447": "boat", "n04273569": "boat", "n03662601": "boat", "n02951358": "boat", "n04612504": "boat", "n04147183": "sailing vessel", "n02981792": "sailing vessel", "n04483307": "sailing vessel", "n03095699": "ship", "n03673027": "ship", "n03947888": "pirate", "n02687172": "aircraft", "n04347754": "submarine", "n04606251": "wreck", "n02860847": "bobsled", "n03218198": "dogsled", "n04336792": "stretcher", "n02917067": "train", "n04487081": "bus", "n03769881": "bus", "n04146614": "school bus", "n02999410": "chain", "n02804414": "baby bed", "n03125729": "baby bed", "n03131574": "baby bed", "n03388549": "bed", "n02870880": "furniture", "n03018349": "furniture", "n03742115": "furniture", "n03016953": "furniture", "n04380533": "lamp", "n03337140": "furniture", "n03891251": "bench", "n02791124": "seat", "n04429376": "seat", "n03376595": "seat", "n04099969": "seat", "n04344873": "sofa", "n04447861": "toilet seat", "n03179701": "desk", "n03201208": "dining table", "n03290653": "furniture", "n04550184": "furniture", "n03998194": "rug", "n04209239": "curtain", "n04418357": "curtain", "n04041544": "radio", "n04404412": "television", "n03733281": "maze", "n02699494": "altar", "n03899768": "patio", "n04311004": "bridge", "n04366367": "bridge", "n04532670": "bridge", "n02793495": "barn", "n03457902": "greenhouse", "n03877845": "palace", "n03781244": "monastery", "n03661043": "library", "n02727426": "apiary", "n02859443": "building", "n03028079": "church", "n03788195": "mosque", "n04346328": "stupa", "n03956157": "planetarium", "n04081281": "restaurant", "n03032252": "cinema", "n03529860": "home theater", "n03697007": "factory", "n03065424": "structure", "n04458633": "structure", "n03837869": "structure", "n02980441": "castle", "n04005630": "prison", "n03461385": "grocery store", "n02776631": "bakery", "n02791270": "barbershop", "n02871525": "bookshop", "n02927161": "shop", "n03089624": "shop", "n04200800": "shop", "n04443257": "shop", "n04462240": "shop", "n03388043": "fountain", "n03776460": "housing", "n03042490": "cliff dwelling", "n04613696": "housing", "n03216828": "dock", "n04486054": "memorial", "n02892201": "memorial", "n03743016": "memorial", "n02788148": "bannister", "n02894605": "barrier", "n03160309": "barrier", "n03000134": "fence", "n03930313": "fence", "n04604644": "fence", "n04326547": "stone wall", "n03459775": "grille", "n04239074": "door", "n04501370": "gate", "n03792972": "tent", "n03530642": "honeycomb", "n03961711": "rack", "n03903868": "structure", "n02814860": "beacon", "n06596364": "magazine", "n04149813": "scoreboard", "n04019541": "puck", "n04599235": "fabric", "n03485794": "fabric", "n03207743": "fabric", "n03887697": "paper towel", "n02808304": "fabric", "n02834397": "fabric", "n04525038": "fabric", "n03724870": "mask", "n03045698": "cloak", "n07248320": "book jacket", "n04201297": "shoji", "n04133789": "shoe", "n04120489": "shoe", "n03680355": "shoe", "n03124043": "shoe", "n03047690": "shoe", "n02786058": "Band Aid", "n04033995": "bedclothes", "n03223299": "doormat", "n04584207": "wig", "n03623198": "knee pad", "n02730930": "apron", "n02669723": "academic gown", "n04532106": "vestment", "n02916936": "bulletproof vest", "n04371430": "swimsuit", "n03710721": "swimsuit", "n02837789": "swimsuit", "n04350905": "suit", "n03325584": "scarf", "n04325704": "scarf", "n02883205": "necktie", "n04591157": "necktie", "n02865351": "neckwear", "n03534580": "garment", "n03770439": "skirt", "n03866082": "skirt", "n04136333": "skirt", "n03980874": "overgarment", "n03404251": "overgarment", "n04479046": "overgarment", "n03630383": "overgarment", "n04370456": "sweater", "n02963159": "sweater", "n03617480": "kimono", "n02667093": "robe", "n03595614": "shirt", "n03188531": "diaper", "n03775071": "glove", "n03127747": "helmet", "n03379051": "helmet", "n02807133": "bathing cap", "n03787032": "mortarboard", "n04209133": "shower cap", "n02869837": "hat", "n02817516": "hat", "n03124170": "hat", "n04259630": "hat", "n03710637": "maillot", "n04254777": "sock", "n03026506": "sock", "n03763968": "military uniform", "n03877472": "pajama", "n03594734": "jean", "n03450230": "dress", "n02892767": "brassiere", "n03929855": "helmet", "n02895154": "armor plate", "n03657121": "lens cap", "n04435653": "roof", "n03220513": "roof", "n04417672": "roof", "n04523525": "roof", "n04590129": "window blind", "n02840245": "binder", "n03637318": "lampshade", "n03788365": "mosquito net", "n04589890": "window screen", "n03347037": "screen", "n03146219": "armor", "n03000247": "armor", "n04192698": "shield", "n03424325": "mask", "n04229816": "mask", "n03527444": "gun", "n04141327": "knife", "n02843684": "birdhouse", "n02825657": "bell cote", "n04507155": "umbrella", "n03717622": "manhole cover", "n02877765": "bottlecap", "n03825788": "nipple", "n03938244": "pillow", "n03483316": "dryer", "n04179913": "sewing machine", "n03584829": "iron", "n03297495": "coffee maker", "n03761084": "microwave", "n03259280": "oven", "n04111531": "oven", "n04442312": "toaster", "n04542943": "home appliance", "n04517823": "vacuum", "n03207941": "dishwasher", "n04070727": "refrigerator", "n04554684": "washer", "n03814906": "neckwear", "n04399382": "teddy", "n04296562": "stage", "n11939491": "flower", "n12057211": "flower", "n13052670": "fungus", "n13044778": "fungus", "n12985857": "fungus", "n13040303": "fungus", "n13037406": "fungus", "n13054560": "fungus", "n12998815": "fungus", "n09835506": "ballplayer", "n10565667": "diver", "n10148035": "groom", "n01768244": "trilobite", "n01770081": "arachnid", "n01770393": "scorpion", "n01773157": "arachnid", "n01773549": "arachnid", "n01773797": "arachnid", "n01774384": "arachnid", "n01774750": "arachnid", "n01775062": "arachnid", "n01776313": "arachnid", "n01784675": "arthropod", "n01990800": "arthropod", "n01978287": "crab", "n01978455": "crab", "n01980166": "crab", "n01981276": "crab", "n01983481": "lobster", "n01984695": "lobster", "n01985128": "crayfish", "n01986214": "crustacean", "n02165105": "beetle", "n02165456": "beetle", "n02167151": "beetle", "n02168699": "beetle", "n02169497": "beetle", "n02172182": "beetle", "n02174001": "beetle", "n02177972": "beetle", "n02190166": "fly", "n02219486": "ant", "n02206856": "bee", "n02226429": "orthopterous insect", "n02229544": "orthopterous insect", "n02231487": "walking stick", "n02233338": "cockroach", "n02236044": "mantis", "n02256656": "insect", "n02259212": "insect", "n02264363": "insect", "n02268443": "dragonfly", "n02268853": "insect", "n02276258": "butterfly", "n02277742": "butterfly", "n02279972": "butterfly", "n02280649": "butterfly", "n02281406": "butterfly", "n02281787": "butterfly", "n01910747": "jellyfish", "n01914609": "anthozoan", "n01917289": "anthozoan", "n01924916": "worm", "n01930112": "worm", "n01943899": "conch", "n01944390": "snail", "n01945685": "snail", "n01950731": "sea slug", "n01955084": "mollusk", "n01968897": "mollusk", "n02317335": "starfish", "n02319095": "echinoderm", "n02321529": "echinoderm", "n02124075": "cat", "n02123394": "cat", "n02123159": "cat", "n02123597": "cat", "n02123045": "cat", "n02100583": "dog", "n02100236": "dog", "n02100735": "dog", "n02101006": "dog", "n02100877": "dog", "n02102973": "dog", "n02102177": "dog", "n02102040": "dog", "n02101556": "dog", "n02101388": "dog", "n02102318": "dog", "n02102480": "dog", "n02099601": "dog", "n02099849": "dog", "n02099429": "dog", "n02099267": "dog", "n02099712": "dog", "n02096294": "dog", "n02095314": "dog", "n02098105": "dog", "n02095889": "dog", "n02095570": "dog", "n02096437": "dog", "n02096051": "dog", "n02098413": "dog", "n02094433": "dog", "n02098286": "dog", "n02097130": "dog", "n02097047": "dog", "n02097209": "dog", "n02093256": "dog", "n02093428": "dog", "n02094114": "dog", "n02096177": "dog", "n02093859": "dog", "n02097298": "dog", "n02096585": "dog", "n02093647": "dog", "n02093991": "dog", "n02097658": "dog", "n02094258": "dog", "n02097474": "dog", "n02093754": "dog", "n02090622": "dog", "n02090721": "dog", "n02092002": "dog", "n02089078": "dog", "n02089867": "dog", "n02089973": "dog", "n02092339": "dog", "n02091635": "dog", "n02088466": "dog", "n02091467": "dog", "n02091831": "dog", "n02088094": "dog", "n02091134": "dog", "n02091032": "dog", "n02088364": "dog", "n02088238": "dog", "n02088632": "dog", "n02090379": "dog", "n02091244": "dog", "n02087394": "dog", "n02110341": "dog", "n02113186": "dog", "n02113023": "dog", "n02113978": "dog", "n02111277": "dog", "n02113712": "dog", "n02113624": "dog", "n02113799": "dog", "n02110806": "dog", "n02111129": "dog", "n02112706": "dog", "n02110958": "dog", "n02109047": "dog", "n02105641": "dog", "n02106382": "dog", "n02106550": "dog", "n02105505": "dog", "n02106030": "dog", "n02106166": "dog", "n02105162": "dog", "n02105056": "dog", "n02105855": "dog", "n02105412": "dog", "n02105251": "dog", "n02106662": "dog", "n02104365": "dog", "n02107142": "dog", "n02110627": "dog", "n02107312": "dog", "n02104029": "dog", "n02110185": "dog", "n02110063": "dog", "n02108089": "dog", "n02108422": "dog", "n02109961": "dog", "n02108000": "dog", "n02107683": "dog", "n02107574": "dog", "n02107908": "dog", "n02109525": "dog", "n02108551": "dog", "n02108915": "dog", "n02112018": "dog", "n02112350": "dog", "n02112137": "dog", "n02111889": "dog", "n02111500": "dog", "n02086910": "dog", "n02086646": "dog", "n02086079": "dog", "n02085936": "dog", "n02087046": "dog", "n02085782": "dog", "n02086240": "dog", "n02085620": "dog", "n02326432": "rabbit", "n02328150": "rabbit", "n02325366": "rabbit", "n02500267": "lemur", "n02497673": "lemur", "n02483708": "ape", "n02483362": "ape", "n02480495": "ape", "n02481823": "ape", "n02480855": "ape", "n02488702": "monkey", "n02484975": "monkey", "n02489166": "monkey", "n02486261": "monkey", "n02486410": "monkey", "n02487347": "monkey", "n02488291": "monkey", "n02493509": "monkey", "n02494079": "monkey", "n02493793": "monkey", "n02492035": "monkey", "n02492660": "monkey", "n02490219": "monkey", "n02132136": "bear", "n02134084": "bear", "n02133161": "bear", "n02134418": "bear", "n02447366": "musteline mammal", "n02442845": "musteline mammal", "n02443484": "musteline mammal", "n02445715": "musteline mammal", "n02441942": "musteline mammal", "n02443114": "musteline mammal", "n02444819": "musteline mammal", "n02509815": "panda", "n02510455": "panda", "n02138441": "viverrine", "n02137549": "viverrine", "n02115913": "wild dog", "n02115641": "wild dog", "n02116738": "wild dog", "n02117135": "hyena", "n02119789": "fox", "n02119022": "fox", "n02120505": "fox", "n02120079": "fox", "n02114712": "wolf", "n02114855": "wolf", "n02114548": "wolf", "n02114367": "wolf", "n02128925": "jaguar", "n02129604": "tiger", "n02128385": "leopard", "n02128757": "snow leopard", "n02129165": "lion", "n02130308": "cheetah", "n02125311": "cougar", "n02127052": "cat", "n02074367": "sea cow", "n02077923": "seal", "n02071294": "dolphin", "n02066245": "whale", "n02391049": "zebra", "n02389026": "horse", "n02437312": "camel", "n02412080": "ram", "n02423022": "antelope", "n02422699": "antelope", "n02422106": "antelope", "n02415577": "wild sheep", "n02417914": "goat", "n02410509": "bovid", "n02408429": "bovid", "n02403003": "ox", "n02398521": "hippopotamus", "n02437616": "llama", "n02396427": "swine", "n02397096": "swine", "n02395406": "swine", "n02457408": "sloth", "n02454379": "armadillo", "n02504458": "elephant", "n02504013": "elephant", "n02346627": "rodent", "n02364673": "rodent", "n02342885": "rodent", "n02356798": "squirrel", "n02361337": "rodent", "n02363005": "beaver", "n01871265": "elephant", "n01872401": "prototherian", "n01873310": "prototherian", "n01882714": "koala", "n01877812": "kangaroo", "n01883070": "wombat", "n01514668": "cock", "n01514859": "hen", "n01518878": "ostrich", "n01530575": "bird", "n01531178": "bird", "n01532829": "bird", "n01534433": "bird", "n01537544": "bird", "n01558993": "bird", "n01560419": "bird", "n01580077": "bird", "n01582220": "bird", "n01592084": "bird", "n01601694": "bird", "n01608432": "bird", "n01614925": "eagle", "n01616318": "bird", "n01622779": "owl", "n01795545": "bird", "n01796340": "bird", "n01797886": "bird", "n01798484": "bird", "n01806143": "peacock", "n01806567": "bird", "n01807496": "bird", "n01817953": "parrot", "n01818515": "parrot", "n01819313": "parrot", "n01820546": "parrot", "n01824575": "bird", "n01828970": "bird", "n01829413": "bird", "n01833805": "bird", "n01843065": "bird", "n01843383": "bird", "n01855672": "goose", "n01847000": "aquatic bird", "n01855032": "aquatic bird", "n01860187": "aquatic bird", "n02002556": "aquatic bird", "n02002724": "aquatic bird", "n02006656": "aquatic bird", "n02007558": "aquatic bird", "n02009912": "aquatic bird", "n02009229": "aquatic bird", "n02011460": "aquatic bird", "n02012849": "aquatic bird", "n02013706": "aquatic bird", "n02018207": "aquatic bird", "n02018795": "aquatic bird", "n02025239": "aquatic bird", "n02027492": "aquatic bird", "n02028035": "aquatic bird", "n02033041": "aquatic bird", "n02037110": "aquatic bird", "n02017213": "aquatic bird", "n02051845": "aquatic bird", "n02056570": "penguin", "n02058221": "bird", "n01664065": "turtle", "n01665541": "turtle", "n01667114": "turtle", "n01667778": "turtle", "n01669191": "turtle", "n01675722": "lizard", "n01677366": "lizard", "n01682714": "lizard", "n01685808": "lizard", "n01687978": "lizard", "n01688243": "lizard", "n01689811": "lizard", "n01692333": "lizard", "n01693334": "lizard", "n01694178": "lizard", "n01695060": "lizard", "n01704323": "dinosaur", "n01698640": "alligator", "n01697457": "crocodile", "n01728572": "snake", "n01728920": "snake", "n01729322": "snake", "n01729977": "snake", "n01734418": "snake", "n01735189": "snake", "n01737021": "snake", "n01739381": "snake", "n01740131": "snake", "n01742172": "snake", "n01744401": "snake", "n01748264": "snake", "n01749939": "snake", "n01751748": "snake", "n01753488": "snake", "n01755581": "snake", "n01756291": "snake", "n01641577": "frog", "n01644373": "frog", "n01644900": "frog", "n01629819": "salamander", "n01630670": "salamander", "n01631663": "salamander", "n01632458": "salamander", "n01632777": "salamander", "n01496331": "ray", "n01498041": "ray", "n01484850": "shark", "n01491361": "shark", "n01494475": "shark", "n02514041": "fish", "n02536864": "fish", "n01440764": "fish", "n01443537": "fish", "n02526121": "fish", "n02606052": "fish", "n02607072": "fish", "n02643566": "fish", "n02655020": "fish", "n02640242": "fish", "n02641379": "fish"
}


# Function to clean and split label text into words
def clean_and_split(text):
    # Remove punctuation and split by spaces
    chars_to_remove = [',', '.', '(', ')', ':', ';', '-', '_']
    for char in chars_to_remove:
        text = text.replace(char, '')
    return text.lower().split()

# # Initialize a dictionary to hold the count of each word
# word_counts = {}

# # Loop through each label, clean, split into words, and count occurrences of each word
# for label in imagenet_labels.values():
#     for word in clean_and_split(label):
#         if word in word_counts:
#             word_counts[word] += 1
#         else:
#             word_counts[word] = 1

# # Sort the word counts dictionary by count in descending order
# sorted_word_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)

# print("Top 10 most frequent words:")
# s = 0
# for word, count in sorted_word_counts:
#     print(f"{word}: {count}")
#     s= s+ count
# print(s)

# List of animals to look for
animals_to_find = ["dog", "cat", "arachnid", "snake", "bird", "monkey", "fish", "beetle", "insect"]

# Initialize a dictionary to hold IDs associated with each animal
animal_ids = {animal: [] for animal in animals_to_find}

# Loop through each label, clean, split into words, and check for animal occurrences
for id, label in imagenet_labels.items():
    words = clean_and_split(label)
    for animal in animals_to_find:
        if animal in words:
            animal_ids[animal].append(id)

# Print IDs associated with each animal
for animal, ids in animal_ids.items():
    if ids:  # Check if the list is not empty
        print(f"IDs associated with {animal}: {', '.join(ids)}")

# Determine the minimum number of IDs among all categories
min_ids = min(len(ids) for ids in animal_ids.values() if ids)

# Randomly select 'n' IDs for each category, where 'n' is the minimum number found
selected_ids = {animal: sample(ids, min_ids) if len(ids) > min_ids else ids for animal, ids in animal_ids.items()}

# Function to copy files from source to destination, creating directories as needed
def copy_files(src_dir, dest_dir, selected_ids):
    for animal, ids in selected_ids.items():
        dest_path = os.path.join(dest_dir, animal)
        os.makedirs(dest_path, exist_ok=True)  # Create the category directory if it doesn't exist
        for id in ids:
            id_path = os.path.join(src_dir, id)
            if os.path.exists(id_path):
                for file in os.listdir(id_path):
                    src_file_path = os.path.join(id_path, file)
                    dest_file_path = os.path.join(dest_path, file)
                    shutil.copy2(src_file_path, dest_file_path)  # Copy each file

# Define your source and destination directories
src_train_dir = "data/train"
src_val_dir = "data/val"
dest_train_dir = "clusteredlabeldata/train"
dest_val_dir = "clusteredlabeldata/val"

# Copy files for both training and validation data
copy_files(src_train_dir, dest_train_dir, selected_ids)
copy_files(src_val_dir, dest_val_dir, selected_ids)
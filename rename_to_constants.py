TOKEN = "YOURTOKENHERE"

#Extra data to gather from the users not provided by Telegram
CUSTOM_FIELDS = [
    "SCHOOL",
    "FIELD",
    "TARGET"
]

#Options to fill the custom fields with
CUSTOM_FIELD_OPTIONS = {
    "SCHOOL":[[["SCI", "SCI"],["ENG", "ENG"]],
             [["ELEC", "ELEC"],["CHEM", "CHEM"]],
             [["BIZ", "BIZ"],["ARTS", "ARTS"]]],
    "SCI":[[["TIK", "TIK"], ["ATHENE", "ATHENE"]],
            [["PRODEKO", "PRODEKO"], ["FK", "FK"]]],
    "ENG":[[["KIK", "KIK"],["IK","IK"]],
            [["MK", "MK"]]],
    "ELEC":[[["AS", "AS"],["SIK","SIK"]],
            [["INKUBIO","INKUBIO"]]],
    "CHEM":[[["PT", "PT"],["KK","KK"]],
            [["PJK","PJK"],["VK","VK"]]],
    "ARTS":[[["AK", "AK"],["NUDE","NUDE"]],
            [["DADA","DADA"],["KOOMA","KOOMA"]]],
    "BIZ":[[["AMS", "AMS"],["ISM","ISM"]],
            [["AE","AE"],["MIB","MIB"]]],

    "HOME":[[["SET SCHOOL", "SCHOOL"]],
            [["SET TARGET", "TARGET"]]]
}

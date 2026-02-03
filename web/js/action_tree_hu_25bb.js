// Auto-generated action tree for hu_25bb
const ACTION_TREE_HU_25BB = {
  "": {
    "position": "SB",
    "spot_name": "SB_toact",
    "actions": [
      {
        "code": "F",
        "type": "FOLD",
        "label": "FOLD",
        "is_hand_end": true
      },
      {
        "code": "C",
        "type": "CALL",
        "label": "CALL",
        "is_hand_end": false
      },
      {
        "code": "R2",
        "type": "RAISE",
        "label": "RAISE",
        "is_hand_end": false
      },
      {
        "code": "RAI",
        "type": "RAISE",
        "label": "ALLIN",
        "is_hand_end": false
      }
    ]
  },
  "C": {
    "position": "BB",
    "spot_name": "SB_C--BB_toact",
    "actions": [
      {
        "code": "X",
        "type": "CHECK",
        "label": "CHECK",
        "is_hand_end": false
      },
      {
        "code": "R3",
        "type": "RAISE",
        "label": "RAISE",
        "is_hand_end": false
      },
      {
        "code": "R7",
        "type": "RAISE",
        "label": "RAISE",
        "is_hand_end": false
      },
      {
        "code": "RAI",
        "type": "RAISE",
        "label": "ALLIN",
        "is_hand_end": false
      }
    ]
  },
  "R2": {
    "position": "BB",
    "spot_name": "SB_R2--BB_toact",
    "actions": [
      {
        "code": "F",
        "type": "FOLD",
        "label": "FOLD",
        "is_hand_end": true
      },
      {
        "code": "C",
        "type": "CALL",
        "label": "CALL",
        "is_hand_end": false
      },
      {
        "code": "R5",
        "type": "RAISE",
        "label": "RAISE",
        "is_hand_end": false
      },
      {
        "code": "R8",
        "type": "RAISE",
        "label": "RAISE",
        "is_hand_end": false
      },
      {
        "code": "RAI",
        "type": "RAISE",
        "label": "ALLIN",
        "is_hand_end": false
      }
    ]
  },
  "RAI": {
    "position": "BB",
    "spot_name": "SB_RAI--BB_toact",
    "actions": [
      {
        "code": "F",
        "type": "FOLD",
        "label": "FOLD",
        "is_hand_end": true
      },
      {
        "code": "C",
        "type": "CALL",
        "label": "CALL",
        "is_hand_end": true
      }
    ]
  },
  "C-R3": {
    "position": "SB",
    "spot_name": "SB_C--BB_R3--SB_toact",
    "actions": [
      {
        "code": "F",
        "type": "FOLD",
        "label": "FOLD",
        "is_hand_end": true
      },
      {
        "code": "C",
        "type": "CALL",
        "label": "CALL",
        "is_hand_end": false
      },
      {
        "code": "R7.5",
        "type": "RAISE",
        "label": "RAISE",
        "is_hand_end": false
      },
      {
        "code": "RAI",
        "type": "RAISE",
        "label": "ALLIN",
        "is_hand_end": false
      }
    ]
  },
  "C-R7": {
    "position": "SB",
    "spot_name": "SB_C--BB_R7--SB_toact",
    "actions": [
      {
        "code": "F",
        "type": "FOLD",
        "label": "FOLD",
        "is_hand_end": true
      },
      {
        "code": "C",
        "type": "CALL",
        "label": "CALL",
        "is_hand_end": false
      },
      {
        "code": "RAI",
        "type": "RAISE",
        "label": "ALLIN",
        "is_hand_end": false
      }
    ]
  },
  "C-RAI": {
    "position": "SB",
    "spot_name": "SB_C--BB_RAI--SB_toact",
    "actions": [
      {
        "code": "F",
        "type": "FOLD",
        "label": "FOLD",
        "is_hand_end": true
      },
      {
        "code": "C",
        "type": "CALL",
        "label": "CALL",
        "is_hand_end": true
      }
    ]
  },
  "R2-R5": {
    "position": "SB",
    "spot_name": "SB_R2--BB_R5--SB_toact",
    "actions": [
      {
        "code": "F",
        "type": "FOLD",
        "label": "FOLD",
        "is_hand_end": true
      },
      {
        "code": "C",
        "type": "CALL",
        "label": "CALL",
        "is_hand_end": false
      },
      {
        "code": "RAI",
        "type": "RAISE",
        "label": "ALLIN",
        "is_hand_end": false
      }
    ]
  },
  "R2-R8": {
    "position": "SB",
    "spot_name": "SB_R2--BB_R8--SB_toact",
    "actions": [
      {
        "code": "F",
        "type": "FOLD",
        "label": "FOLD",
        "is_hand_end": true
      },
      {
        "code": "C",
        "type": "CALL",
        "label": "CALL",
        "is_hand_end": false
      },
      {
        "code": "RAI",
        "type": "RAISE",
        "label": "ALLIN",
        "is_hand_end": false
      }
    ]
  },
  "R2-RAI": {
    "position": "SB",
    "spot_name": "SB_R2--BB_RAI--SB_toact",
    "actions": [
      {
        "code": "F",
        "type": "FOLD",
        "label": "FOLD",
        "is_hand_end": true
      },
      {
        "code": "C",
        "type": "CALL",
        "label": "CALL",
        "is_hand_end": true
      }
    ]
  },
  "C-R3-R7.5": {
    "position": "BB",
    "spot_name": "SB_C--BB_R3--SB_R7_5--BB_toact",
    "actions": [
      {
        "code": "F",
        "type": "FOLD",
        "label": "FOLD",
        "is_hand_end": true
      },
      {
        "code": "C",
        "type": "CALL",
        "label": "CALL",
        "is_hand_end": false
      },
      {
        "code": "RAI",
        "type": "RAISE",
        "label": "ALLIN",
        "is_hand_end": false
      }
    ]
  },
  "C-R3-RAI": {
    "position": "BB",
    "spot_name": "SB_C--BB_R3--SB_RAI--BB_toact",
    "actions": [
      {
        "code": "F",
        "type": "FOLD",
        "label": "FOLD",
        "is_hand_end": true
      },
      {
        "code": "C",
        "type": "CALL",
        "label": "CALL",
        "is_hand_end": true
      }
    ]
  },
  "C-R7-RAI": {
    "position": "BB",
    "spot_name": "SB_C--BB_R7--SB_RAI--BB_toact",
    "actions": [
      {
        "code": "F",
        "type": "FOLD",
        "label": "FOLD",
        "is_hand_end": true
      },
      {
        "code": "C",
        "type": "CALL",
        "label": "CALL",
        "is_hand_end": true
      }
    ]
  },
  "R2-R5-RAI": {
    "position": "BB",
    "spot_name": "SB_R2--BB_R5--SB_RAI--BB_toact",
    "actions": [
      {
        "code": "F",
        "type": "FOLD",
        "label": "FOLD",
        "is_hand_end": true
      },
      {
        "code": "C",
        "type": "CALL",
        "label": "CALL",
        "is_hand_end": true
      }
    ]
  },
  "R2-R8-RAI": {
    "position": "BB",
    "spot_name": "SB_R2--BB_R8--SB_RAI--BB_toact",
    "actions": [
      {
        "code": "F",
        "type": "FOLD",
        "label": "FOLD",
        "is_hand_end": true
      },
      {
        "code": "C",
        "type": "CALL",
        "label": "CALL",
        "is_hand_end": true
      }
    ]
  },
  "C-R3-R7.5-RAI": {
    "position": "SB",
    "spot_name": "SB_C--BB_R3--SB_R7_5--BB_RAI--SB_toact",
    "actions": [
      {
        "code": "F",
        "type": "FOLD",
        "label": "FOLD",
        "is_hand_end": true
      },
      {
        "code": "C",
        "type": "CALL",
        "label": "CALL",
        "is_hand_end": true
      }
    ]
  }
};

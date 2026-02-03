// === Configuration ===
const STACK_DEPTHS = [25, 20, 15, 10];
const GAME_MODES = {
    '3way': { label: '3-Way', folder: '{depth}bb' },
    'hu': { label: 'Heads-Up', folder: 'hu_{depth}bb' },
};

// === State ===
let actions = [];
let currentDepth = 25;
let currentMode = '3way';

// Get action tree for current depth and mode
function getActionTree() {
    if (currentMode === 'hu') {
        const trees = {
            25: typeof ACTION_TREE_HU_25BB !== 'undefined' ? ACTION_TREE_HU_25BB : null,
            20: typeof ACTION_TREE_HU_20BB !== 'undefined' ? ACTION_TREE_HU_20BB : null,
            15: typeof ACTION_TREE_HU_15BB !== 'undefined' ? ACTION_TREE_HU_15BB : null,
            10: typeof ACTION_TREE_HU_10BB !== 'undefined' ? ACTION_TREE_HU_10BB : null,
        };
        return trees[currentDepth];
    } else {
        const trees = {
            25: typeof ACTION_TREE_25BB !== 'undefined' ? ACTION_TREE_25BB : null,
            20: typeof ACTION_TREE_20BB !== 'undefined' ? ACTION_TREE_20BB : null,
            15: typeof ACTION_TREE_15BB !== 'undefined' ? ACTION_TREE_15BB : null,
            10: typeof ACTION_TREE_10BB !== 'undefined' ? ACTION_TREE_10BB : null,
        };
        return trees[currentDepth];
    }
}

function getSpotsFolder() {
    return GAME_MODES[currentMode].folder.replace('{depth}', currentDepth);
}

// === Functions ===
function getActionCodes() {
    return actions.map(a => a.code).join('-');
}

function getSpotFile() {
    const spot = getCurrentSpot();
    return spot ? spot.spot_name : null;
}

function getCurrentSpot() {
    const tree = getActionTree();
    if (!tree) return null;
    const codes = getActionCodes();
    return tree[codes] || null;
}

function getNextPosition() {
    const spot = getCurrentSpot();
    return spot ? spot.position : null;
}

function getAvailableActions() {
    const spot = getCurrentSpot();
    if (!spot) return [];

    return spot.actions.filter(a => !a.is_hand_end).map(a => ({
        code: a.code,
        type: a.type,
        label: formatActionLabel(a.label, a.code),
    }));
}

function formatActionLabel(label, code) {
    if (label === 'FOLD') return 'Fold';
    if (label === 'CALL') return 'Call';
    if (label === 'CHECK') return 'Check';
    if (code === 'RAI') return 'All-in';
    if (code.startsWith('R')) {
        const size = code.substring(1);
        return `Raise ${size}`;
    }
    return label;
}

function getActionClass(type, code) {
    if (type === 'FOLD') return 'fold';
    if (type === 'CALL') return 'call';
    if (type === 'CHECK') return 'check';
    if (type === 'ALLIN' || code === 'RAI') return 'allin';
    return 'raise';
}

function renderUI() {
    const tree = getActionTree();
    if (!tree) {
        document.getElementById('spot-info').textContent = `No data for ${currentDepth}bb`;
        return;
    }

    const selector = document.getElementById('selector');
    selector.innerHTML = '';

    const currentPosition = getNextPosition();

    // Render each action taken
    actions.forEach((a) => {
        const col = createPositionColumn(a.pos, a, false);
        selector.appendChild(col);
    });

    // Add column for current position to act
    if (currentPosition) {
        const col = createPositionColumn(currentPosition, null, true);
        selector.appendChild(col);
    }

    // Update spot info
    const infoEl = document.getElementById('spot-info');
    if (currentPosition) {
        infoEl.textContent = `${currentPosition} to act`;
    } else {
        infoEl.textContent = 'Hand complete';
    }

    // Update matrix
    const spotFile = getSpotFile();
    const frame = document.getElementById('matrix-frame');
    if (spotFile) {
        frame.src = `spots/${getSpotsFolder()}/${spotFile}.html`;
        frame.style.display = 'block';
        document.getElementById('missing-spot')?.remove();
    } else {
        frame.style.display = 'none';
        let msg = document.getElementById('missing-spot');
        if (!msg) {
            msg = document.createElement('div');
            msg.id = 'missing-spot';
            msg.style.cssText = 'padding:20px;color:#888;text-align:center;';
            frame.parentNode.appendChild(msg);
        }
        msg.textContent = currentPosition
            ? `Spot not available: ${getActionCodes() || 'initial'}`
            : 'Hand complete';
    }

    updateControlButtons();
}

function createPositionColumn(pos, actionTaken, isActive) {
    const col = document.createElement('div');
    col.className = 'position-column';
    if (isActive) col.classList.add('active');
    if (actionTaken) col.classList.add('done');

    // Header
    const header = document.createElement('div');
    header.className = 'position-header';

    const posName = document.createElement('span');
    posName.className = 'pos-name';
    posName.textContent = pos;

    const posStack = document.createElement('span');
    posStack.className = 'pos-stack';
    posStack.textContent = pos === 'BTN' ? currentDepth : pos === 'SB' ? (currentDepth - 0.5) : (currentDepth - 1);

    header.appendChild(posName);
    header.appendChild(posStack);
    col.appendChild(header);

    // Actions
    const actionsDiv = document.createElement('div');
    actionsDiv.className = 'position-actions';

    if (actionTaken) {
        const btn = document.createElement('button');
        btn.className = `action-btn ${getActionClass(actionTaken.type, actionTaken.code)} selected`;
        btn.disabled = true;
        btn.textContent = actionTaken.label;
        actionsDiv.appendChild(btn);
    } else if (isActive) {
        const availableActions = getAvailableActions();
        availableActions.forEach(act => {
            const btn = document.createElement('button');
            btn.className = `action-btn ${getActionClass(act.type, act.code)}`;
            btn.textContent = act.label;
            btn.addEventListener('click', () => selectAction(pos, act));
            actionsDiv.appendChild(btn);
        });
    }

    col.appendChild(actionsDiv);
    return col;
}

function selectAction(pos, action) {
    actions.push({
        pos,
        code: action.code,
        type: action.type,
        label: action.label,
    });
    renderUI();
}

function back() {
    if (actions.length > 0) {
        actions.pop();
        renderUI();
    }
}

function reset() {
    actions = [];
    renderUI();
}

function setDepth(depth) {
    currentDepth = depth;
    actions = [];

    // Update button states
    document.querySelectorAll('.stack-btn').forEach(btn => {
        btn.classList.toggle('active', parseInt(btn.dataset.depth) === depth);
    });

    renderUI();
}

function setMode(mode) {
    currentMode = mode;
    actions = [];

    // Update button states
    document.querySelectorAll('.mode-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.mode === mode);
    });

    renderUI();
}

function updateControlButtons() {
    const backBtn = document.getElementById('back-btn');
    if (backBtn) {
        backBtn.disabled = actions.length === 0;
    }
}

// === Init ===
document.querySelectorAll('.stack-btn').forEach(btn => {
    btn.addEventListener('click', () => setDepth(parseInt(btn.dataset.depth)));
});

document.querySelectorAll('.mode-btn').forEach(btn => {
    btn.addEventListener('click', () => setMode(btn.dataset.mode));
});

renderUI();

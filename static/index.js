function createCard(card, cb) {
    const c = document.createElement("div");
    c.classList.add("card");

    const link = document.createElement(cb !== undefined ? "a" : "span");
    link.innerText = card.name;
    if (cb) {
        link.addEventListener("click", cb);
        link.href = "#"
    }
    c.appendChild(link);
    
    const health = document.createElement("span");
    health.innerText = "Health: " + card.defense.toString();
    c.appendChild(health)

    const manaCost = document.createElement("span");
    manaCost.innerText = "Mana Cost: " + card.manaCost.toString();
    c.appendChild(manaCost)

    const damage = document.createElement("span");
    damage.innerText = "Damage: " + card.damage.toString();
    c.appendChild(damage)

    const priority = document.createElement("span");
    priority.innerText = "Priority: " + (-card.priority).toString();
    c.appendChild(priority)

    return c;
}

class Client {
    async refreshUI() {
        this.getHand();
        this.getPlayerInfo();
        this.getActive();

        const gs = await this.getGameState();
        console.log(gs.turnCounter + 1)
        document.getElementById("counter").innerText = (gs.turnCounter + 1).toString();

        const myInfo = document.getElementById("myInfo");
        const oppInfo = document.getElementById("oppInfo");

        if (gs.currentPlayer === this.player) {
            myInfo.classList.add("currentPlayer");
            oppInfo.classList.remove("currentPlayer");
        } else {
            oppInfo.classList.add("currentPlayer");
            myInfo.classList.remove("currentPlayer");
        }

    }

    async getGameState() {
        return await (await fetch("/getState")).json()
    }

    async endTurn() {
        await fetch("/endTurn?player=" + this.player.toString())
        this.refreshUI();
    }

    async getPlayerInfo() {
        let myInfo = await (await fetch("/getPlayerInfo?player=" + this.player.toString())).json();
        let oppInfo = await (await fetch("/getPlayerInfo?player=" + ((this.player + 1) % 2).toString())).json();

        document.getElementById("health").innerText = myInfo.health;
        document.getElementById("mana").innerText = myInfo.mana;
        document.getElementById("opphealth").innerText = oppInfo.health;
        document.getElementById("oppmana").innerText = oppInfo.mana;
    }

    async getHand() {
        this.hand = await (await fetch("/getHand?player=" + this.player.toString())).json();
        const hand = document.getElementById("handCont");
        hand.innerText = "";
        this.hand.forEach((item, idx) => {
            hand.appendChild(createCard(item, this.playCard.bind(this, idx)));
        })
    }

    async getActive() {
        this.active[0] = await (await fetch("/getActive?player=0")).json();
        this.active[1] = await (await fetch("/getActive?player=1")).json();

        console.log(this.active);

        document.getElementById("active").innerText = "";
        this.active[this.player].forEach(item => {
            document.getElementById("active").appendChild(createCard(item));
        })

        const gs = await this.getGameState();
        // if (gs.end[(this.player + 1) % 2]) {
        document.getElementById("oppActive").innerText = "";
        this.active[(this.player + 1) % 2].forEach(item => {
            document.getElementById("oppActive").appendChild(createCard(item));
        })
        // }
    }

    async playCard(card) {
        await fetch("/playCard?player=" + this.player.toString() + "&card=" + card.toString());
        this.getActive()
        this.getHand()
        this.getPlayerInfo()
    }
    
    async register() {
        this.player = (await (await fetch("/register")).json())?.player;

        if (this.player > -1) {
            this.refreshUI()
        }
    }

    constructor() {
        this.player = -1;
        this.hand = [];
        this.active = [[], []];

        this.register()
        this.getPlayerInfo()
    }
}

const client = new Client();
document.getElementById("end").addEventListener("click", () => {
    client.endTurn();
});

setInterval(async () => {
    const gs = await client.getGameState();
    client.refreshUI()
    if (gs.gameOver) {
        if (gs.winner === client.player) {
            // redirect to win page
            location.href = "/static/win.html"
        } else {
            location.href = "/static/lose.html"
        }
    }
}, 5000)
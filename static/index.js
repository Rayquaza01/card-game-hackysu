class Client {
    async getHand() {
        this.hand = await (await fetch("/getHand?player=" + this.player.toString())).json();
    }

    async getActive() {
        this.active[0] = await (await fetch("/getHand?player=0")).json();
        this.active[1] = await (await fetch("/getHand?player=1")).json();
    }

    async playCard(card) {
        await fetch("/playCard?player=" + this.player.toString() + "&card=" + card.toString());
        this.getActive()
    }
    
    async register() {
        this.player = (await (await fetch("/register")).json())?.player;

        if (this.player > -1) {
            this.getHand()
        }
    }

    constructor() {
        this.player = -1;
        this.hand = [];
        this.active = [[], []];

        this.register()
    }
}
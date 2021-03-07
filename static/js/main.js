class OpenMenu{
    constructor(){
        this.DOM = {};
        this.DOM.btn = document.querySelector('.mobile-menu__btn');
        this.DOM.cross= document.querySelectorAll('.fa-times');
        this.DOM.side = document.querySelector('.ctg-lists');
        this.DOM.container = document.querySelector('#global-container');
        this.eventType= this._getEventType();
        this._addEvent1();
        this._addEvent2();
    }


    _getEventType(){
        return window.ontouchstart ? 'touchstart' : 'click'
    }

    _toggle(){
        this.DOM.container.classList.toggle('menu-open')
    }

    _remove(){
        this.DOM.drop.classList.remove('dropDown')
    }

    _addEvent1() {
        this.DOM.btn.addEventListener(this.eventType, this._toggle.bind(this));
        if(this.DOM.side !== null){
            this.DOM.side.addEventListener(this.eventType, this._toggle.bind(this));
        }
        // this.DOM.cross.addEventListener(this.eventType, this._toggle.bind(this));
        // this.DOM.btn.addEventListener(this.eventType, this._remove.bind(this));
        // this.DOM.side.addEventListener(this.eventType, this._remove.bind(this));
    }
    _addEvent2() {
        for (let i = 0; i < this.DOM.cross.length; i++) {
            this.DOM.cross[i].addEventListener(this.eventType, function(){
                // this.DOM.container.classList.toggle('menu-open').bind(this);
                // this.DOM.container.classList.toggle('menu-open'); ←エラーの理由不明
                document.querySelector('#global-container').classList.toggle('menu-open');
                });
            }
    }


}

new OpenMenu();

class DorpDown{
    constructor(){
        this.DOM = {};
        this.DOM.drop = document.querySelectorAll('.category-menu__item > span');
        this.DOM.mDrop = document.querySelectorAll('.mobile-menu__link');
        this.eventType= this._getEventType();
        this._addEvent1();
        this._addEvent2();
        this._addEvent3();
        // this._addEvent4();
        
    }

    _getEventType(){
        return window.ontouchstart ? 'touchstart' : 'click'
    }

    _addEvent1() {
        for (let i = 0; i < this.DOM.drop.length; i++) {
        this.DOM.drop[i].addEventListener(this.eventType, function(){
            this.classList.toggle('dropDown');
            this.nextElementSibling.classList.toggle('dropDown');
        });
        }
    }

    _addEvent2() {
    　　if(this.DOM.mDrop[3] !== null){
        this.DOM.mDrop[3].addEventListener(this.eventType, function(){
            this.classList.toggle('dropDown');
            this.nextElementSibling.classList.toggle('dropDown');
        });
    }
    } 

    _addEvent3() {
        　　if(this.DOM.mDrop[4] !== null){
            this.DOM.mDrop[4].addEventListener(this.eventType, function(){
                this.classList.toggle('dropDown');
                this.nextElementSibling.classList.toggle('dropDown');
            });
        }
        }
    
    // _addEvent4() {
    //         if(document.getElementById('menu-open') == null){
    //             if(this.DOM.mDrop[3] !== null){
    //                 this.DOM.mDrop[3].addEventListener(this.eventType, function(){
    //                     this.classList.remove('dropDown');
    //                     this.nextElementSibling.classList.remove('dropDown');
    //                 });
    //             }
    //             if(this.DOM.mDrop[4] !== null){
    //                 this.DOM.mDrop[4].addEventListener(this.eventType, function(){
    //                     this.classList.remove('dropDown');
    //                     this.nextElementSibling.classList.remove('dropDown');
    //                 });

    //             }
    
    //         }
    // }
}

new DorpDown();

class TextAnimation {
    constructor() {
        this.DOM = {};
        this.DOM.el = document.querySelector('.inview');
        if(this.DOM.el !== null){
            this.chars = this.DOM.el.innerHTML.trim().split("");
            console.log(this.chars);
            this.DOM.el.innerHTML = this._splitText();
        }    
}
    _splitText() {
        return this.chars.reduce((acc, curr) => {
            curr = curr.replace(/\s+/, '&nbsp;');
            return `${acc}<span class="char">${curr}</span>`;
        }, "");
    }

}

new TextAnimation();

class Trophy{
    constructor(){
        const color = ['gold','silver','bronze'];
        this.DOM = {};
        this.DOM.rank = document.querySelectorAll('.ranking-order');
        if(this.DOM.rank !== null){
            for (let i = 0; i < this.DOM.rank.length; i++) {
               if(i < 3){
                this.DOM.rank[i].classList.add('fa');
                this.DOM.rank[i].classList.add('fa-trophy');
                this.DOM.rank[i].classList.add(color[i]);
               }else{
                this.DOM.rank[i].innerHTML=i + 1 +".";
               }
            }   
        }
    }

}

new Trophy();
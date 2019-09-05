
          // The Slideshow class.
      class Slideshow {
          constructor(el) {
              
              this.DOM = {el: el};
            
              this.config = {
                slideshow: {
                  delay: 3000,
                  pagination: {
                    duration: 3,
                  }
                }
              };
              
              // Set the slideshow
              this.init();
            
          }
          init() {
            
            var self = this;
            
            // Charmed title
            this.DOM.slideTitle = this.DOM.el.querySelectorAll('.slide-title');
            this.DOM.slideTitle.forEach((slideTitle) => {
              charming(slideTitle);
            });
            
            // Set the slider
            this.slideshow = new Swiper (this.DOM.el, {
                
                loop: true,
                autoplay: {
                  delay: this.config.slideshow.delay,
                  disableOnInteraction: false,
                },
                speed: 500,
                preloadImages: true,
                updateOnImagesReady: true,
                
                // lazy: true,
                // preloadImages: false,
      
                pagination: {
                  el: '.slideshow-pagination',
                  clickable: true,
                  bulletClass: 'slideshow-pagination-item',
                  bulletActiveClass: 'active',
                  clickableClass: 'slideshow-pagination-clickable',
                  modifierClass: 'slideshow-pagination-',
                  renderBullet: function (index, className) {
                    
                    var slideIndex = index,
                        number = (index <= 8) ? '0' + (slideIndex + 1) : (slideIndex + 1);
                    
                    var paginationItem = '<span class="slideshow-pagination-item">';
                    paginationItem += '<span class="pagination-number">' + number + '</span>';
                    paginationItem = (index <= 8) ? paginationItem + '<span class="pagination-separator"><span class="pagination-separator-loader"></span></span>' : paginationItem;
                    paginationItem += '</span>';
                  
                    return paginationItem;
                    
                  },
                },
      
                // Navigation arrows
                navigation: {
                  nextEl: '.slideshow-navigation-button.next',
                  prevEl: '.slideshow-navigation-button.prev',
                },
      
                // And if we need scrollbar
                scrollbar: {
                  el: '.swiper-scrollbar',
                },
              
                on: {
                  init: function() {
                    self.animate('next');
                  },
                }
              
              });
            
              // Init/Bind events.
              this.initEvents();
              
          }
          initEvents() {
              
              this.slideshow.on('paginationUpdate', (swiper, paginationEl) => this.animatePagination(swiper, paginationEl));
              //this.slideshow.on('paginationRender', (swiper, paginationEl) => this.animatePagination());
      
              this.slideshow.on('slideNextTransitionStart', () => this.animate('next'));
              
              this.slideshow.on('slidePrevTransitionStart', () => this.animate('prev'));
                  
          }
          animate(direction = 'next') {
            
              // Get the active slide
              this.DOM.activeSlide = this.DOM.el.querySelector('.swiper-slide-active'),
              this.DOM.activeSlideImg = this.DOM.activeSlide.querySelector('.slide-image'),
              this.DOM.activeSlideTitle = this.DOM.activeSlide.querySelector('.slide-title'),
              this.DOM.activeSlideTitleLetters = this.DOM.activeSlideTitle.querySelectorAll('span');
            
              // Reverse if prev  
              this.DOM.activeSlideTitleLetters = direction === "next" ? this.DOM.activeSlideTitleLetters : [].slice.call(this.DOM.activeSlideTitleLetters).reverse();
            
              // Get old slide
              this.DOM.oldSlide = direction === "next" ? this.DOM.el.querySelector('.swiper-slide-prev') : this.DOM.el.querySelector('.swiper-slide-next');
              if (this.DOM.oldSlide) {
                // Get parts
                this.DOM.oldSlideTitle = this.DOM.oldSlide.querySelector('.slide-title'),
                this.DOM.oldSlideTitleLetters = this.DOM.oldSlideTitle.querySelectorAll('span'); 
                // Animate
                this.DOM.oldSlideTitleLetters.forEach((letter,pos) => {
                  TweenMax.to(letter, .3, {
                    ease: Quart.easeIn,
                    delay: (this.DOM.oldSlideTitleLetters.length-pos-1)*.04,
                    y: '50%',
                    opacity: 0
                  });
                });
              }
            
              // Animate title
              this.DOM.activeSlideTitleLetters.forEach((letter,pos) => {
                TweenMax.to(letter, .6, {
                  ease: Back.easeOut,
                  delay: pos*.05,
                  startAt: {y: '50%', opacity: 0},
                  y: '0%',
                  opacity: 1
                });
              });
            
              // Animate background
              TweenMax.to(this.DOM.activeSlideImg, 1.5, {
                  ease: Expo.easeOut,
                  startAt: {x: direction === 'next' ? 200 : -200},
                  x: 0,
              });
            
              //this.animatePagination()
          
          }
          animatePagination(swiper, paginationEl) {
                  
            // Animate pagination
            this.DOM.paginationItemsLoader = paginationEl.querySelectorAll('.pagination-separator-loader');
            this.DOM.activePaginationItem = paginationEl.querySelector('.slideshow-pagination-item.active');
            this.DOM.activePaginationItemLoader = this.DOM.activePaginationItem.querySelector('.pagination-separator-loader');
            
            console.log(swiper.pagination);
            // console.log(swiper.activeIndex);
            
            // Reset and animate
              TweenMax.set(this.DOM.paginationItemsLoader, {scaleX: 0});
              TweenMax.to(this.DOM.activePaginationItemLoader, this.config.slideshow.pagination.duration, {
                startAt: {scaleX: 0},
                scaleX: 1,
              });
            
            
          }
          
      }
      
      const slideshow = new Slideshow(document.querySelector('.slideshow'));
      
     
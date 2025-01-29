let currentIndex = 0;
	
		function moveSlide(direction) {
			const sliderWrapper = document.querySelector('.slider-wrapper');
			const slideWidth = 300 + 32; // Width of one box + gap
			const visibleSlides = 3; // Number of visible slides at a time
			const totalSlides = document.querySelectorAll('.fea-box').length;
	
			// Update index based on direction
			currentIndex += direction;
	
			// Loop back to start or end
			if (currentIndex > totalSlides - visibleSlides) {
				currentIndex = 0; // Go back to the first slide
			} else if (currentIndex < 0) {
				currentIndex = totalSlides - visibleSlides; // Go to the last set of slides
			}
	
			// Move the slider
			sliderWrapper.style.transform = `translateX(-${currentIndex * slideWidth}px)`;
		}

        // ----------------------------------------------------------------------------------

        // Show menu links on burger click
		$('#menu-btn').click(function(){
			$('nav .navigation ul').addClass('active')
		});

		// Hide navbar on click function
		$('#menu-close').click(function(){
			$('nav .navigation ul').removeClass('active')
		});

		document.querySelectorAll('.read-more-btn').forEach(button => {
			button.addEventListener('click', () => {
				const fullContent = button.previousElementSibling;
				if (fullContent.style.display === 'block') {
					fullContent.style.display = 'none';
					button.textContent = 'Read More';
				} else {
					fullContent.style.display = 'block';
					button.textContent = 'Read Less';
				}
			});
		});
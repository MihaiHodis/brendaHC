var myCarousel = document.querySelector('#testimonialCarousel');
var carousel = new bootstrap.Carousel(myCarousel, {
  interval: 5000, // Intervalul la care se schimbă slide-urile (3 secunde)
  ride: 'carousel', // Activează schimbarea automată a slide-urilor
  pause: 'hover',   // Pauzează pe hover pentru o experiență mai bună
  wrap: true        // După ultimul slide revine la primul
});

    /*
     * Open the drawer when the menu ison is clicked.
     */

    var menu = document.querySelector('#menu');
    var main = document.querySelector('main');
    var drawer = document.querySelector('.nav');

    menu.addEventListener('click', function (e) {
      drawer.classList.toggle('open');
      e.stopPropagation();
    });

    main.addEventListener('click', function() {
      drawer.classList.remove('open');
    });

    function myFunction(x) {
      x.classList.toggle("change");
    }

/**
* Typical Observer's registration
*/

document.addEventListener("DOMContentLoaded", function() {
  var lazyImages = document.querySelectorAll("img.lazy");
  const config = {
    root: null, // avoiding 'root' or setting it to 'null' sets it to default value: viewport
    rootMargin: '0px',
    threshold: 0.5
  };

  if ("IntersectionObserver" in window) {
    let lazyImageObserver = new IntersectionObserver(function(entries, observer) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          let lazyImage = entry.target;
          lazyImage.src = lazyImage.dataset.src;
          lazyImage.srcset = lazyImage.dataset.srcset;
          lazyImage.classList.remove("lazy");
          lazyImageObserver.unobserve(lazyImage);
        }
      });
    },config);

    lazyImages.forEach(function(lazyImage) {
      lazyImageObserver.observe(lazyImage);
    });
  } else {
    // Possibly fall back to a more compatible method here
  }
});


if ('serviceWorker' in navigator) {
  console.log("Will the service worker register?");
  navigator.serviceWorker.register('sw.js', {scope:'/'})
    .then(function(reg){
      console.log("Yes, it did.");
    }).catch(function(err) {
      console.log("No it didn't. This happened: ", err)
    });
}


// if ('serviceWorker' in navigator) {
//   navigator.serviceWorker.register('/sw.js', {
//           scope: '/'
//       })
//       .then(function(reg) {
//           if (!navigator.serviceWorker.controller) {
//               return;
//           }
//           // there is updated service worker ready and waiting to to take over
//           if (reg.waiting) {
//               updateReady(reg.waiting)
//               return;
//           }
//           // there is update on the way. Although may be  be thrown away if installation fails we will listen to the stat

//           if (reg.installing) {
//               trackInstalling(reg.installing)
//               return;
//           }

//           reg.addEventListener('updatefound', function() {
//               trackInstalling(reg.installing)
//           });
//       });
// }

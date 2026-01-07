// Mobile navigation helper: toggles side-navbar and overlay
(function() {
  document.addEventListener('DOMContentLoaded', function() {
    var hamburger = document.querySelector('.hamburger');
    var side = document.querySelector('.side-navbar');

    console.log('Mobile nav loaded');
    console.log('Hamburger found:', hamburger);
    console.log('Side navbar found:', side);

    if (!hamburger || !side) {
      console.log('Hamburger or side-navbar not found, exiting');
      return;
    }

    // Create overlay
    var overlay = document.createElement('div');
    overlay.className = 'mobile-overlay';
    overlay.style.position = 'fixed';
    overlay.style.top = '0';
    overlay.style.left = '0';
    overlay.style.right = '0';
    overlay.style.bottom = '0';
    overlay.style.background = 'rgba(0,0,0,0.5)';
    overlay.style.zIndex = '998';
    overlay.style.display = 'none';
    overlay.style.opacity = '0';
    overlay.style.transition = 'opacity 0.3s ease';
    document.body.appendChild(overlay);

    function openNav() {
      console.log('Opening nav');
      side.classList.add('active');
      hamburger.classList.add('active');
      overlay.style.display = 'block';
      setTimeout(function() { overlay.style.opacity = '1'; }, 10);
      document.body.style.overflow = 'hidden';
    }

    function closeNav() {
      console.log('Closing nav');
      side.classList.remove('active');
      hamburger.classList.remove('active');
      overlay.style.opacity = '0';
      setTimeout(function() { overlay.style.display = 'none'; }, 300);
      document.body.style.overflow = '';
    }

    // Toggle on hamburger click
    hamburger.onclick = function(e) {
      e.preventDefault();
      e.stopPropagation();
      console.log('Hamburger clicked, active:', side.classList.contains('active'));
      if (side.classList.contains('active')) {
        closeNav();
      } else {
        openNav();
      }
    };

    // Close on overlay click
    overlay.onclick = function() {
      closeNav();
    };

    // Close nav when clicking a link (only on mobile)
    var links = side.querySelectorAll('a');
    for (var i = 0; i < links.length; i++) {
      links[i].onclick = function() {
        if (window.innerWidth <= 1024) {
          closeNav();
        }
      };
    }

    // Close on Escape key
    document.onkeydown = function(e) {
      if (e.key === 'Escape' && side.classList.contains('active')) {
        closeNav();
      }
    };

    // Handle resize - close mobile nav when resizing to desktop
    window.onresize = function() {
      if (window.innerWidth > 1024) {
        side.classList.remove('active');
        hamburger.classList.remove('active');
        overlay.style.display = 'none';
        overlay.style.opacity = '0';
        document.body.style.overflow = '';
      }
    };

    console.log('Mobile nav setup complete');
  });
})();
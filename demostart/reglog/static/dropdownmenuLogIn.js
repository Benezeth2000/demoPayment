document.addEventListener('DOMContentLoaded', function() {
  var dropbtn = document.querySelector('.dropbtn');
  var dropdownContent = document.querySelector('.dropdown-content');

  dropbtn.addEventListener('click', function() {
    dropdownContent.style.display = dropdownContent.style.display === 'none' ? 'block' : 'none';
  });
});


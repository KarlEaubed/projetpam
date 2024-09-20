function openNav() {
    document.getElementById("sidebar1").style.width = "500px";
}
    
function closeNav() {
    document.getElementById("sidebar1").style.width = "0";
}

document.getElementById('colorPicker1').addEventListener('change', function() {
    var color = this.value;
    document.querySelector('.navbar-custom-1').style.backgroundColor = color;
});

document.getElementById('colorPicker2').addEventListener('change', function() {
    var color = this.value;
    document.querySelector('.navbar-custom-2').style.backgroundColor = color;
});

document.getElementById('fontFamilySelector').addEventListener('change', function() {
    var fontFamily = this.value;
    document.querySelectorAll('.navbar-custom-1 .nav-item a:not(.exclude-color-change)').forEach(function(navItem) {
        navItem.style.fontFamily = fontFamily;
    });
    document.querySelectorAll('.navbar-custom-1 .navbar-brand').forEach(function(navBrand) {
        navBrand.style.fontFamily = fontFamily;
    });

    document.querySelectorAll('.navbar-custom-2 .nav-item a:not(.exclude-color-change)').forEach(function(navItem) {
        navItem.style.fontFamily = fontFamily;
    });
    document.querySelectorAll('.navbar-custom-2 .navbar-brand').forEach(function(navBrand) {
        navBrand.style.fontFamily = fontFamily;
    });
});

document.getElementById('fontColorPicker').addEventListener('change', function() {
    var color = this.value;
    document.querySelectorAll('.navbar-custom-1 .nav-item a:not(.exclude-color-change)').forEach(function(navItem) {
        navItem.style.color = color;
    });
    document.querySelectorAll('.navbar-custom-1 .navbar-brand').forEach(function(navBrand) {
        navBrand.style.color = color;
    });

    document.querySelectorAll('.navbar-custom-2 .nav-item a:not(.exclude-color-change)').forEach(function(navItem) {
        navItem.style.color = color;
    });
    document.querySelectorAll('.navbar-custom-2 .navbar-brand').forEach(function(navBrand) {
        navBrand.style.color = color;
    });
});

document.getElementById('fontSizeSlider').addEventListener('change', function() {
    var fontSize = this.value + 'px';
    document.querySelectorAll('.navbar-custom-1 .nav-item a:not(.exclude-color-change)').forEach(function(navItem) {
        navItem.style.fontSize = fontSize;
    });
    document.querySelectorAll('.navbar-custom-1 .navbar-brand').forEach(function(navBrand) {
        navBrand.style.fontSize = fontSize;
    });

    document.querySelectorAll('.navbar-custom-2 .nav-item a:not(.exclude-color-change)').forEach(function(navItem) {
        navItem.style.fontSize = fontSize;
    });
    document.querySelectorAll('.navbar-custom-2 .navbar-brand').forEach(function(navBrand) {
        navBrand.style.fontSize = fontSize;
    });
});
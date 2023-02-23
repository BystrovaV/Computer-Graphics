// ---------------------------- НАСТРОЙКА COLOR PICKER -----------------------------------
var colorPicker = new iro.ColorPicker('#picker', {
  width: 266,
  layoutDirection: 'vertical',
  layout: [
    
    { 
      component: iro.ui.Box,
      options: {}
    },
    { 
      component: iro.ui.Slider,
      options: {
        sliderType: 'hue'
      }
    },
  ]
});

// ---------------------------- НАСТРОЙКА ПАЛИТРЫ -----------------------------------

var swatchGrid = document.getElementById('swatch-grid');

swatchGrid.addEventListener('click', function(e) {
  var clickTarget = e.target;
  if (clickTarget.dataset.color) {
    colorPicker.color.set(clickTarget.dataset.color);
  }
});

// ---------------------------- ИНИЦИАЛИЗАЦИЯ ПЕРЕМЕННЫХ -----------------------------------

var selected = document.getElementById('formats');

var rgb = {'R':255, 'G':255, 'B':255};
var hsv = {'H':360, 'S':100, 'V':100};
var lab = {'L':100, 'a':128, 'b':128};

var color_1 = document.getElementById('color_1');
var color_2 = document.getElementById('color_2');
var color_3 = document.getElementById('color_3');

var another_format_1 = document.getElementById("text-another-format-1");
var another_format_2 = document.getElementById("text-another-format-2");
var another_format_3 = document.getElementById("text-another-format-3");

var attention = document.getElementById("attention");
var pickedColor = document.getElementById("picked-color");

color_1.value = rgb.R;
color_2.value = rgb.G;
color_3.value = rgb.B;

colorPicker.on(['color:change', 'color:init'], onColorChange);

function onColorChange(color) {
  attention.innerText = "";

  rgb.R = color.rgb.r;
  rgb.G = color.rgb.g;
  rgb.B = color.rgb.b;

  pickedColor.style.backgroundColor = "rgb(" + rgb.R + ", " + rgb.G + ", " + rgb.B + ")";

  var xyz;

  rgb_to_hsv();
  xyz = rgb_to_xyz();
  xyz_to_lab(xyz);

  setup();
}

function outAnotherFormats() {
  another_format_1.value = Math.round(rgb.R) + ", " + Math.round(rgb.G) + ", " + Math.round(rgb.B);
  another_format_2.value = Math.round(hsv.H) + ", " + Math.round(hsv.S * 100) + "%, " +  Math.round(hsv.V * 100) + "%";
  another_format_3.value = Math.round(lab.L) + ", " + Math.round(lab.a) + ", " +  Math.round(lab.b);
}

function setup() {
  if(selected.value == 'RGB') {
    color_1.value = rgb.R;
    color_2.value = rgb.G;
    color_3.value = rgb.B;

    outAnotherFormats();
  } else if (selected.value == 'HSV') {
    color_1.value = Math.round(hsv.H);
    color_2.value = Math.round(hsv.S * 100);
    color_3.value = Math.round(hsv.V * 100);

    outAnotherFormats();
  } else if (selected.value == "LAB") {
    color_1.value = Math.round(lab.L);
    color_2.value = Math.round(lab.a);
    color_3.value = Math.round(lab.b);

    outAnotherFormats();
  }
}

function validateColors() {
  if (selected.value == "RGB") {
    if (color_1.valueAsNumber <= 255 && color_1.value >= 0 && 
      color_2.valueAsNumber <= 255 && color_2.value >= 0 && 
      color_3.valueAsNumber <= 255 && color_3.value >= 0)
      return true;
  } else if (selected.value == "HSV") {
    if (color_1.valueAsNumber <= 360 && color_1.value >= 0 && 
      color_2.valueAsNumber <= 100 && color_2.value >= 0 && 
      color_3.valueAsNumber <= 100 && color_3.value >= 0)
      return true;
  } else if (selected.value == "LAB") {
    if (color_1.valueAsNumber <= 100 && color_1.value >= 0 && 
      color_2.valueAsNumber <= 128 && color_2.value >= -128 && 
      color_3.valueAsNumber <= 128 && color_3.value >= -128)
      return true;
  }

  return false;
}

function getSelectedFormat() {
  rgb.R = colorPicker.color.rgb.r;
  rgb.G = colorPicker.color.rgb.g;
  rgb.B = colorPicker.color.rgb.b;

  var xyz;

  var label_1 = document.getElementById('label-1');
  var label_2 = document.getElementById('label-2');

  var l1 = document.getElementById('label_1');
  var l2 = document.getElementById('label_2');
  var l3 = document.getElementById('label_3');

  rgb_to_hsv();
  xyz = rgb_to_xyz();
  xyz_to_lab(xyz);

  setup();
  if (selected.value == "RGB") {
    color_1.min = 0;
    color_1.max = 255;
    color_2.min = 0;
    color_2.max = 255;
    color_3.min = 0;
    color_3.max = 255;

    label_1.innerText = "HSV";
    label_2.innerText = "Lab";

    l1.innerText = "R";
    l2.innerText = "G";
    l3.innerText = "B";
  } else if (selected.value == "HSV") {
    color_1.min = 0;
    color_1.max = 360;
    color_2.min = 0;
    color_2.max = 100;
    color_3.min = 0;
    color_3.max = 100;
    
    label_1.innerText = "RGB";
    label_2.innerText = "Lab";

    l1.innerText = "H";
    l2.innerText = "S";
    l3.innerText = "V";
  } else if (selected.value == "LAB") {
    color_1.min = 0;
    color_1.max = 100;
    color_2.min = -128;
    color_2.max = 128;
    color_3.min = -128;
    color_3.max = 128;

    label_1.innerText = "RGB";
    label_2.innerText = "HSV";

    l1.innerText = "L";
    l2.innerText = "A";
    l3.innerText = "B";
  }
}

function changeColor() {
  attention.innerText = "";

  var xyz;

  if (!validateColors()) {
    another_format_1.value = "Undefined";
    another_format_2.value = "Undefined";
    return;
  }

  if (selected.value == 'RGB') {
    colorPicker.color.rgb = {'r': color_1.valueAsNumber, 'g': color_2.valueAsNumber, 'b': color_3.valueAsNumber};

    rgb.R = color_1.valueAsNumber;
    rgb.G = color_2.valueAsNumber;
    rgb.B = color_3.valueAsNumber;

    rgb_to_hsv();
    xyz = rgb_to_xyz();
    xyz_to_lab(xyz);

    outAnotherFormats();
  } else if (selected.value == 'HSV') {
    hsv.H = color_1.valueAsNumber;
    hsv.S = color_2.valueAsNumber / 100.0;
    hsv.V = color_3.valueAsNumber / 100.0;

    hsv_to_rgb();

    colorPicker.off('color:change', onColorChange);
    colorPicker.color.rgb = {'r': rgb.R, 'g': rgb.G, 'b': rgb.B};
    colorPicker.on('color:change', onColorChange);

    xyz = rgb_to_xyz();
    xyz_to_lab(xyz);

    outAnotherFormats();
  } else if (selected.value == 'LAB') {
    lab.L = color_1.valueAsNumber;
    lab.a = color_2.valueAsNumber;
    lab.b = color_3.valueAsNumber;

    xyz = lab_to_xyz();
    xyz_to_rgb(xyz);

    rgb_to_hsv();

    colorPicker.off('color:change', onColorChange);
    colorPicker.color.rgb = {'r': rgb.R, 'g': rgb.G, 'b': rgb.B};
    colorPicker.on('color:change', onColorChange);

    outAnotherFormats();
  }

  pickedColor.style.backgroundColor = "rgb(" + rgb.R + ", " + rgb.G + ", " + rgb.B + ")";
}

function rgb_to_hsv() {
  var new_rgb = {'R':rgb.R / 255, 'G':rgb.G / 255, 'B':rgb.B / 255};

  var cmax = Math.max(new_rgb.R, new_rgb.G, new_rgb.B);
  var cmin = Math.min(new_rgb.R, new_rgb.G, new_rgb.B);

  var delta = cmax - cmin;

  if (delta == 0) {
    hsv.H = 0;
  } else if (cmax == new_rgb.R) {
    hsv.H = 60 * (((new_rgb.G - new_rgb.B) / delta) % 6);
  } else if (cmax == new_rgb.G) {
    hsv.H = 60 * ((new_rgb.B - new_rgb.R) / delta + 2);
  } else if (cmax == new_rgb.B) {
    hsv.H = 60 * ((new_rgb.R - new_rgb.G) / delta + 4);
  }
  if (hsv.H < 0)
    hsv.H += 360;

  if (cmax == 0) {
    hsv.S = 0;
  } else {
    hsv.S = delta / cmax;
  }

  hsv.V = cmax;
}

// hsv = {"H": 0, "S": 10 / 100, "V": 100 / 100};
// var rgb = {'R':255, 'G':255, 'B':255};
// hsv_to_rgb();
// console.log(rgb);

function hsv_to_rgb() {
  var M = 255 * hsv.V;
  var m = M * (1 - hsv.S);

  var z = (M - m) * (1 - Math.abs((hsv.H / 60)%2 - 1));

  if (0 <= hsv.H && hsv.H < 60) {
    rgb.R = M;
    rgb.G = z + m;
    rgb.B = m;
  } else if (60 <= hsv.H && hsv.H < 120) {
    rgb.R = z + m;
    rgb.G = M;
    rgb.B = m;
  } else if (120 <= hsv.H && hsv.H < 180) {
    rgb.R = m;
    rgb.G = M;
    rgb.B = z + m;
  } else if (180 <= hsv.H && hsv.H < 240) {
    rgb.R = m;
    rgb.G = z + m;
    rgb.B = M;
  } else if (240 <= hsv.H && hsv.H < 300) {
    rgb.R = z + m;
    rgb.G = m;
    rgb.B = M;
  } else if (300 <= hsv.H && hsv.H < 360) {
    rgb.R = M;
    rgb.G = m;
    rgb.B = z + m;
  }
//-------------------------------------------------------------------
  // rgb.R = Math.round(rgb.R);
  // rgb.G = Math.round(rgb.G);
  // rgb.B = Math.round(rgb.B);
}

function rgb_to_xyz() {
  var Rn = fx_to_xyz(rgb.R / 255) * 100;
  var Gn = fx_to_xyz(rgb.G / 255) * 100;
  var Bn = fx_to_xyz(rgb.B / 255) * 100;

  // var xyz = {'X': Math.round(0.412453 * Rn + 0.357580 * Gn + 0.180423 * Bn),
  //           'Y': Math.round(0.212671 * Rn + 0.715160 * Gn + 0.072169 * Bn),
  //           'Z': Math.round(0.019334 * Rn + 0.119193 * Gn + 0.950227 * Bn)};
  var xyz = {'X': 0.412453 * Rn + 0.357580 * Gn + 0.180423 * Bn,
  'Y': 0.212671 * Rn + 0.715160 * Gn + 0.072169 * Bn,
  'Z': 0.019334 * Rn + 0.119193 * Gn + 0.950227 * Bn};

  return xyz;
}

function fx_to_xyz(x) {
  if (x >= 0.04045) {
    return Math.pow((x + 0.055)/1.055, 2.4);
  }

  return x / 12.92;
}

function xyz_to_rgb(xyz) {
  
  var Rn = 3.2406 * xyz.X / 100 - 1.5372 * xyz.Y / 100 - 0.4986 * xyz.Z / 100;
  var Gn = -0.9689 * xyz.X / 100 + 1.8758 * xyz.Y / 100 + 0.0415 * xyz.Z / 100;
  var Bn = 0.0557 * xyz.X / 100 - 0.2040 * xyz.Y / 100 + 1.0570 * xyz.Z / 100;
//---------------------------------------------------------------------
  rgb.R = fx_to_rgb(Rn) * 255;
  if (rgb.R > 255 || rgb.R < 0 || rgb.G > 255 || rgb.G < 0 || rgb.B > 255 || rgb.B < 0)
    attention.innerText = "Произошло обрезание значения при переводе из Lab в RGB!";

  rgb.R = rgb.R > 255 ? 255 : rgb.R;
  rgb.R = rgb.R < 0 ? 0 : rgb.R;

  rgb.G = fx_to_rgb(Gn) * 255;
  rgb.G = rgb.G > 255 ? 255 : rgb.G;
  rgb.G = rgb.G < 0 ? 0 : rgb.G;

  rgb.B = fx_to_rgb(Bn) * 255;
  rgb.B = rgb.B > 255 ? 255 : rgb.B;
  rgb.B = rgb.B < 0 ? 0 : rgb.B;
  // console.log(xyz);
  //---------------------------------------------------------------------
  // rgb.R = fx_to_rgb(Rn) * 255;
  // rgb.G = fx_to_rgb(Gn) * 255;
  // rgb.B = fx_to_rgb(Bn) * 255;
}

function fx_to_rgb(x) {
  if (x >= 0.0031308) {
    return 1.055 * Math.pow(x, 1 / 2.4) - 0.055;
  }

  return 12.92 * x;
}

function xyz_to_lab(xyz) {
  var white = {'X': 95.047, 'Y': 100, 'Z': 108.883};

  lab.L = 116 * fx_xyz_to_lab(xyz.Y / white.Y) - 16;
  lab.a = 500 * (fx_xyz_to_lab(xyz.X / white.X) - fx_xyz_to_lab(xyz.Y / white.Y));
  lab.b = 200 * (fx_xyz_to_lab(xyz.Y / white.Y) - fx_xyz_to_lab(xyz.Z / white.Z));

  return lab;
}

function fx_xyz_to_lab(x) {
  if (x >= 0.008856) {
    return Math.pow(x, 1/3);
  }

  return 7.787 * x + 16 / 116;
}

function lab_to_xyz() {
  console.log(lab);
  var white = {'X': 95.047, 'Y': 100, 'Z': 108.883};

  var xyz = {
    'X': fx_lab_to_xyz(lab.a / 500 + (lab.L + 16) / 116) * white.X,
    'Y': fx_lab_to_xyz((lab.L + 16)/116) * white.Y,
    'Z': fx_lab_to_xyz((lab.L + 16)/116 - lab.b/ 200) * white.Z
  };

  console.log(xyz);

  return xyz;
}

function fx_lab_to_xyz(x) {
  if (Math.pow(x, 3) >= 0.008856) {
    return Math.pow(x, 3);
  }

  return (x - 16 / 116) / 7.787;

}

function copy(button) {
  var copyText;
  var tooltip;
  
  if (button.id == "btn-1") {
    copyText = document.getElementById("text-another-format-1");
    tooltip = document.getElementById("myTooltip-1");
  } else if (button.id == "btn-2") {
    copyText = document.getElementById("text-another-format-2");
    tooltip = document.getElementById("myTooltip-2");
  } else if (button.id == "btn-3") {
    copyText = document.getElementById("text-another-format-3");
    tooltip = document.getElementById("myTooltip-3");
  }else {
    return;
  }

  // Select the text field
  copyText.select();
  copyText.setSelectionRange(0, 99999); // For mobile devices

  // Copy the text inside the text field
  navigator.clipboard.writeText(copyText.value);
  
  
  tooltip.innerHTML = "Copied!";
}

function outCopy(tooltip) {
  // var tooltip = document.getElementsByClassName("");
  tooltip.children[0].innerText = "Copy to clipboard";
  // tooltip.innerHTML = "Copy to clipboard";
}
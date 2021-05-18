chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
  chrome.tabs.sendMessage(
    tabs[0].id,
    { from: "popup", subject: "getData" },
    insertData
  );
});

chrome.tabs.query(
  { active: true, windowId: chrome.windows.WINDOW_ID_CURRENT },
  function (tabs) {
    var url_val = tabs[0].url;
    chrome.storage.local.set({ url: url_val });
  }
);


//Get Price

var productDescription = () => {
	if(document.getElementById('productDescription')){
		
		var section = document.getElementById('productDescription');
		var descrp = section.getElementsByTagName('p')[0].innerText;
		
	return descrp; 
} 
else if (document.getElementById('unqualified')){
	var section = document.getElementById('unqualified');
	var availableFrom = section.getElementsByClassName('a-color-price')[0].innerText;
	return availableFrom;

} else if (document.getElementById('outOfStock')) {
	return "Out Of Stock";

} else if (document.getElementById('unqualifiedBuyBox')){
	return "See Buying Options";

} else if (document.getElementById('priceblock_saleprice')){
	var price = document.getElementById('priceblock_saleprice').innerText;
	
	return price;
} else
  return 'N/A'

}

document.addEventListener("DOMContentLoaded", function () {
 console.log( productDescription())

  const home = document.getElementById("defaultOpen");
  const about = document.getElementById("about");
  const showabout = document.getElementById("showabout");
  const showhome = document.getElementById("showhome");
  const btn = document.getElementById("rating");
  const loading = document.getElementById("loading");
  home.addEventListener("click", function () {
    console.log("insidehome");
    showabout.classList.add("d-none");
    showhome.classList.remove("d-none");
    showhome.classList.add("show-results");
     about.classList.remove('selected');
    home.classList.add('selected')
  });
  about.addEventListener("click", function () {
    console.log("insideabout");
    showabout.classList.remove("d-none");
    showhome.classList.add("d-none");
    showabout.classList.add("show-results");
    about.classList.add('selected');
    home.classList.remove('selected')
  });
  btn.addEventListener("click", function () {
    btn.style.display = "none";
    loading.classList.remove("d-none");
    chrome.storage.local.get("url", function (result) {
      sendURL({ URL: result.url });
    });
  });
  renderStars();
});

const colorStars = (data) => {
  const { people, planet, animal, total } = data;
  const checkedClass = "text-success";

  for (let i = 0; i < parseInt(people, 10); i++) {
    const star = document.getElementById(`people-${i}`);
    star.classList.add(checkedClass);
  }

  for (let i = 0; i < parseInt(planet, 10); i++) {
    const star = document.getElementById(`planet-${i}`);
    star.classList.add(checkedClass);
  }

  for (let i = 0; i < parseInt(animal, 10); i++) {
    const star = document.getElementById(`animal-${i}`);
    star.classList.add(checkedClass);
  }

  for (let i = 0; i < parseInt(total, 10); i++) {
    const star = document.getElementById(`tr-${i}`);
    star.classList.add(checkedClass);
  }
};

const createStar = (id) => {
  const i = document.createElement("i");
  i.id = id;
  i.classList.add("fab");
  i.classList.add("fa-envira");

  return i;
};

const generateStars = (MAX_STARS, entity) => {
  const stars = [];
  for (let i = 0; i < MAX_STARS; i++) {
    stars.push(createStar(`${entity}-${i}`));
  }
  return stars;
};

const renderStars = () => {
  const MAX_STARS = 5;
  const totalRatingDiv = document.getElementById("total-rating");
  const peopleDiv = document.getElementById("rating-people");
  const planetDiv = document.getElementById("rating-planet");
  const animalDiv = document.getElementById("rating-animal");
  const peopleStars = generateStars(MAX_STARS, "people");
  const planetStars = generateStars(MAX_STARS, "planet");
  const animalStars = generateStars(MAX_STARS, "animal");
  const totalRatingStars = generateStars(MAX_STARS, "tr");

  for (let s of peopleStars) {
    peopleDiv.appendChild(s);
  }

  for (let s of planetStars) {
    planetDiv.appendChild(s);
  }

  for (let s of animalStars) {
    animalDiv.appendChild(s);
  }

  for (let s of totalRatingStars) {
    totalRatingDiv.appendChild(s);
  }
};

const avg = (array) => array.reduce((a, b) => a + b) / array.length;

const sendURL = async (url) => {
  const error = document.getElementById("error");
  const results = document.getElementById("results-div");
  const loading = document.getElementById("loading");
  error.classList.add("d-none");

  try {
    const res = await axios.post("http://socolab.luddy.indiana.edu:13693/scrape", [url]);
    colorStars({ ...res.data, total: avg(Object.values(res.data)) });
    results.classList.add("show-results");
    loading.classList.add("d-none");
  } catch (err) {
    error.classList.remove("d-none");
    console.log(err);
  }
};

function insertData(data) {
  document.getElementById("title").innerHTML = data.title;
  // document.getElementById('asin').innerHTML = prediction_vals;
  // document.getElementById('ratings').innerHTML = "hi";
}

const newPost = {
  statement:
    "This puts us in a unique position to truly represent our diverse community of outdoor enthusiasts. We are committed to ensure diversity in all our ranks as we grow",
};

// const sendRequest = async () => {
//     try {
//         const resp = await axios.post('http://127.0.0.1:12345/prediction', newPost);
//         console.log(resp.data);
//     } catch (err) {
//         // Handle Error Here
//         console.error(err);
//     }

// document.addEventListener('DOMContentLoaded', function () {
//     var btn = document.getElementById('rating');
//     btn.addEventListener('click', function() {
//     sendRequest();

//     });
// });

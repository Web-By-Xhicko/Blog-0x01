let moreUrl = document.querySelector('.More_Url')
let sideProfile = document.querySelector('.SideProfile')
moreUrl.addEventListener('click', ()=>{
    sideProfile.classList.toggle('OpenSideProfile')
    categoryList.classList.remove('CatList')
  })

let openCategory = document.querySelector('.OpenCategoryList')
let categoryList = document.querySelector('.CategoryList')
openCategory.addEventListener('click', ()=>{
    categoryList.classList.toggle('CatList')
    sideProfile.classList.remove('OpenSideProfile')
})

let openCategory2 = document.querySelector('.OpenCategoryList2')
let categoryList2 = document.querySelector('.CategoryList2')
openCategory2.addEventListener('click', ()=>{
    categoryList2.classList.toggle('CatList2')
})


let Close = document.querySelectorAll('.Close')
let disappear = document.querySelectorAll('.Disappear')
Close.forEach((closeBtn, index) => {
    closeBtn.addEventListener('click', () => {
    disappear[index].classList.toggle('remove');
    });
});

let moreUrl = document.querySelector('.More_Url')
let sideProfile = document.querySelector('.SideProfile')
let openCategory = document.querySelector('.OpenCategoryList')
let categoryList = document.querySelector('.CategoryList')
let openCategory2 = document.querySelector('.OpenCategoryList2')
let categoryList2 = document.querySelector('.CategoryList2')


moreUrl.addEventListener('click', ()=>{
    sideProfile.classList.toggle('OpenSideProfile')
    categoryList.classList.remove('CatList')
  })

openCategory.addEventListener('click', ()=>{
    categoryList.classList.toggle('CatList')
    sideProfile.classList.remove('OpenSideProfile')
})

openCategory2.addEventListener('click', ()=>{
    categoryList2.classList.toggle('CatList2')
})


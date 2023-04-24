let revOpts = document.getElementById('RevOpts')
function RevOpts(){
    revOpts.classList.toggle('active')
}


let moreUrl = document.querySelector('.More_Url')
let sideProfile = document.querySelector('.SideProfile')
let openCategory = document.querySelector('.OpenCategoryList')
let categoryList = document.querySelector('.CategoryList')

moreUrl.addEventListener('click', ()=>{
    sideProfile.classList.toggle('OpenSideProfile')
    categoryList.classList.remove('CatList')
  })

openCategory.addEventListener('click', ()=>{
    categoryList.classList.toggle('CatList')
    sideProfile.classList.remove('OpenSideProfile')
})
import NProgress from "nprogress"

NProgress.configure({     
    easing: 'ease',
    speed: 500,  
    showSpinner: false,    
    trickleSpeed: 200, 
    minimum: 0.3,
	//color: 'F48FB1'
})

export default NProgress;
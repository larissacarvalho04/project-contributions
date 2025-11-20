# RSS Reader Prototype — Node.js

![Node.js](https://img.shields.io/badge/Node.js-18+-339933?logo=node.js&logoColor=white)
![Express](https://img.shields.io/badge/Express.js-minimal-000000?logo=express&logoColor=white)
![RSS](https://img.shields.io/badge/RSS-Parser-FFA500?logo=rss&logoColor=white)

## Description
This folder contains the **initial prototype** of an RSS reader built with **Node.js**.  
It fetches the RSS feed from the STJ website and displays the results in a simple frontend using HTML/CSS/JS.

⚠️ **Important:**  
This version contains **only my individual work**.  
Later modifications done during the **team project** were not added here.

---

## Features (based only on this prototype)
- Fetch RSS posts from STJ  
- Render the results on a simple HTML page  
- Basic client-side search and filtering  
- Minimal backend using Express  

(No AWS S3, no deploy, no loaders — only what exists in this prototype.)

---

## Folder Structure
```
.
├── public/
│   ├── index.html        
│   ├── style.css         
│   └── script.js         
│
├── services/
│   ├── rssService.js     
│   └── s3Service.js      
│
└── utils/
    └── server.js
```

---


## Notes
- This is only the **prototype** version I built individually.  
- Final team adaptations were based on this structure but **are not included**.

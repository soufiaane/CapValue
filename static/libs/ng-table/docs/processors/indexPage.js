<<<<<<< HEAD
module.exports = function indexPageProcessor(){
    return{
        $runBefore:['rendering-docs'],
        $runAfter:['componentsDataProcessor'],
        $process:function(docs){
            docs.push({
                template:'index.template.html',
                outputPath:'index.html',
                path:'index.html'
            })
        }
    }
};
=======
module.exports = function indexPageProcessor(){
    return{
        $runBefore:['rendering-docs'],
        $runAfter:['componentsDataProcessor'],
        $process:function(docs){
            docs.push({
                template:'index.template.html',
                outputPath:'index.html',
                path:'index.html'
            })
        }
    }
};
>>>>>>> 942286391f24f61d690faaf4c33948109167ed24

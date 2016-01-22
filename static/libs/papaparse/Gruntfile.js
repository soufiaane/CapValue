<<<<<<< HEAD
module.exports = function(grunt) {
	grunt.initConfig({
		uglify: {
			options: {
				preserveComments: 'some',
			},
			min: {
				files: {
					'papaparse.min.js': ['papaparse.js']
				},
			},
		},
	});

	grunt.loadNpmTasks('grunt-contrib-uglify');

	grunt.registerTask('build', ['uglify']);
}
=======
module.exports = function(grunt) {
	grunt.initConfig({
		uglify: {
			options: {
				preserveComments: 'some',
			},
			min: {
				files: {
					'papaparse.min.js': ['papaparse.js']
				},
			},
		},
	});

	grunt.loadNpmTasks('grunt-contrib-uglify');

	grunt.registerTask('build', ['uglify']);
}
>>>>>>> 942286391f24f61d690faaf4c33948109167ed24

const { createApp } = Vue;
createApp({
	delimiters: ['[[', ']]'],
	mixins: [window.mix ? window.mix : {}],
	data() {
		return {
			catalog_category: {},
			main_search: '',
		};
	},
	methods: {
		getCatalogCategories() {
			axios
				.get('http://0.0.0.0:8000/api/catalog_category')
				.then((response) => {
					this.catalog_category = response.data;
				})
				.catch((error) => {
					console.log(error);
					this.errored = true;
				})
				.finally(() => (this.loading = false));
		},
		submitMainSearch() {
			window.location.replace(`/catalog?product__name__icontains=${this.main_search}`);
		},
	},
	mounted() {
		this.getCatalogCategories();
	},
}).mount('#app');

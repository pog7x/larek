const { createApp } = Vue;
createApp({
	delimiters: ['[[', ']]'],
	mixins: [window.mix ? window.mix : {}],
	data() {
		return {
			catalogCategory: {},
			mainSearch: '',
		};
	},
	methods: {
		getCatalogCategories() {
			axios
				.get('http://0.0.0.0:8000/api/catalog_category')
				.then((response) => {
					this.catalogCategory = response.data;
				})
				.catch((error) => {
					console.log(error);
					this.errored = true;
				})
				.finally(() => (this.loading = false));
		},
		submitMainSearch() {
			window.location.replace(`/catalog?product__name__icontains=${this.mainSearch}`);
		},
		createCart(payload) {
			axios
				.post('http://0.0.0.0:8000/api/cart', payload)
				.catch((error) => {
					console.log(error);
					this.errored = true;
				})
				.finally(() => (this.loading = false));
		},
	},
	mounted() {
		this.getCatalogCategories();
	},
}).mount('#app');

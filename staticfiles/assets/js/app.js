const { createApp } = Vue;
createApp({
	delimiters: ['[[', ']]'],
	mixins: [window.mix ? window.mix : {}],
	data() {
		return {
			catalogCategories: [],
			mainSearch: '',
		};
	},
	components: {
		categories: {
			template:
				'<div class="CategoriesButton-link" v-for="(cc, index) in ccategories" :key="index"> \
							<a :href="`/catalog?product__catalog_category__id=${cc.id}`"> \
								<div class="CategoriesButton-icon"> \
									<img :src="[[ cc.icon ]]" :alt="[[ cc.name ]]" style="max-width: 23px; max-height: 19px;"/> \
								</div> \
								<span class="CategoriesButton-text">{{ cc.name }}</span> \
							</a> \
						</div>',
			props: ['ccategories'],
		},
	},
	methods: {
		getCookie(name) {
			let cookieValue = null;
			if (document.cookie && document.cookie !== '') {
				const cookies = document.cookie.split(';');
				for (let i = 0; i < cookies.length; i++) {
					const cookie = cookies[i].trim();
					// Does this cookie string begin with the name we want?
					if (cookie.substring(0, name.length + 1) === name + '=') {
						cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
						break;
					}
				}
			}
			return cookieValue;
		},
		getCatalogCategories() {
			axios
				.get('http://0.0.0.0:8000/api/catalog_category')
				.then((response) => {
					this.catalogCategories = response.data;
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
		async createCart(productSellerID, productsCount) {
			axios.defaults.xsrfCookieName = 'csrftoken';
			axios.defaults.xsrfHeaderName = 'X-CSRFToken';
			await axios
				.post(
					'http://0.0.0.0:8000/api/cart',
					{ product_seller_id: productSellerID, products_count: productsCount },
					{
						headers: {
							Accept: 'application/json',
							'Content-Type': 'application/json',
						},
						withCredentials: true,
					}
				)
				.then(async () => {
					this.product = await this.fetchProduct(prodID);
				})
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

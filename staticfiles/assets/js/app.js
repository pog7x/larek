const { createApp } = Vue;
const app = createApp({
	delimiters: ['[[', ']]'],
	mixins: [window.mix ? window.mix : {}],
	data() {
		return {
			catalogCategories: [],
			mainSearch: '',
			cartTotalData: {
				total_products_count: 0,
				total_products_price: 0,
			},
			cartIcon: '',
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
		carttotal: {
			template: `
						<a class="CartBlock-block" href="/cart">
							<img class="CartBlock-img" :src="carticon" alt="To cart" />
							<span class="CartBlock-amount">{{ carttotaldata.total_products_count }}</span>
						</a>
						<div class="CartBlock-block"><span class="CartBlock-price">{{ carttotaldata.total_products_price.toLocaleString() }}&nbsp;$</span></div>
					`,
			props: ['carttotaldata', 'carticon'],
		},
	},
	methods: {
		getCatalogCategories() {
			this.axios
				.get('/api/catalog_category')
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
			await this.axios.post('/api/cart', { product_seller_id: productSellerID, products_count: productsCount });
		},
		async getUserCarts() {
			let resp = await this.axios.get('/api/cart');
			return resp.data;
		},
		async getCartTotal() {
			let resp = await this.axios.get('/api/cart_total');
			return resp.data;
		},
	},
	async mounted() {
		this.getCatalogCategories();
		this.cartTotalData = await this.getCartTotal();
		this.cartIcon = cartIcon;
	},
});

function getCookie(name) {
	let cookieValue = null;
	if (document.cookie && document.cookie !== '') {
		const cookies = document.cookie.split(';');
		for (let i = 0; i < cookies.length; i++) {
			const cookie = cookies[i].trim();
			if (cookie.substring(0, name.length + 1) === name + '=') {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}

const axiosInstance = axios.create({
	xsrfCookieName: 'csrftoken',
	xsrfHeaderName: 'X-CSRFToken',
	withCredentials: true,
	headers: {
		Accept: 'application/json',
		'Content-Type': 'application/json',
		'X-Sessionid': getCookie('sessionid'),
	},
});

app.config.globalProperties.axios = {
	...axiosInstance,
};

app.mount('#app');

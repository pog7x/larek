var mix = {
	data() {
		return {
			comment_text: null,
			loading: false,
			errored: false,
			product: {},
			price: null,
			product_seller: null,
		};
	},
	async mounted() {
		const urlSearchParams = new URLSearchParams(window.location.search);
		const params = Object.fromEntries(urlSearchParams.entries());
		this.product_seller = params.product_seller;
		this.product = await this.fetchProduct(prod_id);

		for (const ps of this.product.product_seller) {
			this.price = ps.price.toLocaleString();
			if (ps.id == this.product_seller) {
				break;
			}
		}
	},
	methods: {
		async createReviewAndFetchProduct() {
			await this.createReview();
			this.comment_text = null;
		},
		async fetchProduct(id) {
			try {
				const response = await axios.get(`http://0.0.0.0:8000/api/product/${id}`);
				return response.data;
			} catch (error) {
				this.errored = true;
			}
		},
		async createReview() {
			await axios
				.post('http://0.0.0.0:8000/api/review', { comment: this.comment_text, user_id: 1, product_id: prod_id })
				.then(async () => {
					this.product = await this.fetchProduct(prod_id);
				})
				.catch((error) => {
					console.log(error);
					this.errored = true;
				})
				.finally(() => (this.loading = false));
		},
	},
};

var mix = {
	data() {
		return {
			commentText: null,
			loading: false,
			errored: false,
			product: {},
			price: null,
			productSeller: null,
			activePhoto: 0,
		};
	},
	async mounted() {
		const urlSearchParams = new URLSearchParams(window.location.search);
		const params = Object.fromEntries(urlSearchParams.entries());
		this.productSeller = params.productSeller;
		this.product = await this.fetchProduct(prodID);

		for (const ps of this.product.product_seller) {
			this.price = ps.price.toLocaleString();
			if (ps.id == this.productSeller) {
				break;
			}
		}
	},
	methods: {
		setActivePhoto(index) {
			this.activePhoto = index;
		},
		async createReviewAndFetchProduct() {
			await this.createReview();
			this.commentText = null;
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
				.post('http://0.0.0.0:8000/api/review', { comment: this.commentText, user_id: 1, product_id: prodID })
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
};

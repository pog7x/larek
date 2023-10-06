var mix = {
	data() {
		return {
			review: { commentText: null },
			loading: false,
			errored: false,
			product: {},
			price: null,
			productSellerID: null,
			activePhoto: 0,
			userCarts: [],
			cartProductsCount: 0,
		};
	},
	async mounted() {
		const urlSearchParams = new URLSearchParams(window.location.search);
		const params = Object.fromEntries(urlSearchParams.entries());
		this.productSellerID = params.product_seller;
		this.product = await this.fetchProduct(prodID);
		this.userCarts = await this.getUserCarts({ product_seller_id: this.productSellerID });
		this.cartProductsCount = this.userCarts[0]?.products_count;
		for (const ps of this.product.product_seller) {
			this.price = ps.price.toLocaleString();
			if (ps.id == this.productSellerID) {
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
			this.review.commentText = null;
		},
		async fetchProduct(id) {
			try {
				let response = await this.axios.get(`/api/product/${id}`);
				return response.data;
			} catch (error) {
				this.errored = true;
			}
		},
		async createReview() {
			await this.axios
				.post('/api/review', { comment: this.review.commentText, product_id: prodID })
				.then(async () => {
					this.product = await this.fetchProduct(prodID);
				})
				.catch((error) => {
					console.log(error);
					this.errored = true;
				})
				.finally(() => (this.loading = false));
		},
		async createProductCart() {
			let cart = await this.createCart(this.productSellerID, 0);
			this.userCarts[0] = cart;
			this.cartProductsCount = this.userCarts[0]?.products_count;
			this.cartTotalData = await this.getCartTotal();
		},
		async updateProductCartCount(newRes = null) {
			try {
				let cart = await this.updateCartByID(this.userCarts[0].id, { products_count: newRes });
				this.userCarts[0].products_count = cart.products_count;
			} catch (err) {
			} finally {
				this.cartTotalData = await this.getCartTotal();
				this.cartProductsCount = this.userCarts[0].products_count;
			}
		},
		async incrementProductCartCount() {
			try {
				let newRes = Number(this.userCarts[0].products_count) + 1;
				await this.updateProductCartCount(newRes);
			} catch (err) {
				this.cartProductsCount = this.carts[0].products_count;
			}
		},
		async decrementProductCartCount() {
			try {
				let newRes = Number(this.userCarts[0].products_count) - 1;
				await this.updateProductCartCount(newRes);
			} catch (err) {
				this.cartProductsCount = this.carts[0].products_count;
			}
		},
	},
};

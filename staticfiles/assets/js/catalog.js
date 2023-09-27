var mix = {
	data() {
		return {
			query: {
				price__gte: '1',
				price__lte: '50000',
				product__name__icontains: '',
				in_stock: '',
				ordering: '-product__views_history__count',
				page: 1,
			},
			maxCount: 1,
			productSellers: null,
			loading: false,
			errored: false,
			orderBy: [
				{ id: 'product__views_history__count', title: 'Популярности' },
				{ id: 'product__review__count', title: 'Отзывам' },
				{ id: 'product__id', title: 'Новизне' },
				{ id: 'price', title: 'Цене' },
			],
			orderDir: '-',
			orderDirMap: {
				'': 'dec',
				'-': 'inc',
			},
		};
	},
	mounted() {
		const urlSearchParams = new URLSearchParams(window.location.search);
		const params = Object.fromEntries(urlSearchParams.entries());
		this.query = { ...this.query, ...params };
		this.orderDir = this.query.ordering.startsWith('-') ? '-' : '';
		this.changePage(this.query.page);
		this.updateSearch();
		this.fetchProductSeller();
	},
	methods: {
		filterForm() {
			this.query.price__gte = document.querySelector('input[name=price__gte]').value;
			this.query.price__lte = document.querySelector('input[name=price__lte]').value;
			this.updateSearch();
			this.fetchProductSeller();
		},
		fetchProductSeller() {
			this.axios
				.get('/api/product_seller', {
					params: { ...this.query },
				})
				.then((response) => {
					this.productSellers = response.data.results;
					this.maxCount = response.data.count;
				})
				.catch((error) => {
					console.log(error);
					this.errored = true;
				})
				.finally(() => (this.loading = false));
		},
		setSort(id) {
			this.orderDir = this.orderDir === '-' && this.query.ordering.endsWith(id) ? '' : '-';
			this.query.ordering = `${this.orderDir}${id}`;
			this.updateSearch();
			this.fetchProductSeller();
		},
		updateSearch() {
			const newSearch = new URLSearchParams([...Object.entries(this.query)]).toString();
			window.history.replaceState(null, null, `?${newSearch}`);
		},
		changePage(param) {
			const newPage = Number(param);
			const maxPages = Math.ceil(Number(this.maxCount) / 9);
			if (newPage <= 0 || newPage > maxPages) {
				this.query.page = 1;
			} else {
				this.query.page = newPage;
			}
			this.fetchProductSeller();
			this.updateSearch();
		},
	},
};

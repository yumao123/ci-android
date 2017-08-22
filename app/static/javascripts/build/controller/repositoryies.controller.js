/*
	打包配置页面控制器
*/
angular
	.module("buiploy.building")
	.controller("RepositoryiesController", RepositoryiesController);

RepositoryiesController.$inject = ["$scope", "$rootScope", "$interval", "BussinessService", "$modal", "$log", ]

function RepositoryiesController($scope, $rootScope, $interval, BussinessService, $modal, $log){
	/*
		页码初始化
	*/
	$scope.paginationConf = {
		currentPage: 1,
		itemsPerPage: 10,
	};

	/*
		初始化表格label
	*/
	var GetTableColumns = function(){
		var postData = {
			item_name : "repositoryModule"
		};

		var postUrl = "/api/get_tableTitle";

		BussinessService.list(postData, postUrl).success(function(response){
			$scope.tableConf.colums = response.columns

			$scope.$watch('paginationConf.currentPage + paginationConf.itemsPerPage', GetTableRows);
		});
	};

	/*
		获取表格数据
	*/
	var GetTableRows = function(){
		var postData = {
			item_name : "repositoryModule",
			pageIndex: $scope.paginationConf.currentPage,
			pageSize: $scope.paginationConf.itemsPerPage
		};

		var postUrl = "/api/get_tableInfo";

		BussinessService.list(postData, postUrl).success(function (response) {
			$scope.paginationConf.totalItems = response.count;
			$scope.repository_list = response.data_list;

			//package rows -> cells
			$scope.tableConf.rows = []
			for (var i= 0; i < $scope.repository_list.length; i++){
				$scope.tableConf.rows.push({cells: []});
				for (var x=0; x < $scope.tableConf.colums.length; x++){
					var key = $scope.tableConf.colums[x].name
					$scope.tableConf.rows[i].cells.push($scope.repository_list[i][key])
					//判断本行的数据是否成功
					$scope.tableConf.rows[i].issuccess = $scope.repository_list[i]['issuccess']
				}
			}
		});
	}

	$scope.add_repository = function(){
		var modalInstance = $modal.open({
			templateUrl : "/api/template/modal_repository_add",
			controller: "AddRepositoryModalInstanceCtrl",
			size: 'lg',
			backdrop: 'static',											
			resolve: {
				modal_info: function(){
					return {
						modal_name: '缓存代码',
						GetTableRows: GetTableRows,
					};
				},
			},
		});		

	};

	/*
		初始化表格
	*/
	$scope.tableConf = {
		id: "android_table",
		class: "table table-bordered table-hover",
		getColumns: GetTableColumns,
		clickFunc: null,
	}


}


angular
	.module("buiploy.building")
	.controller("AddRepositoryModalInstanceCtrl", AddRepositoryModalInstanceCtrl);

AddRepositoryModalInstanceCtrl.$inject = ["$scope", "$modalInstance", "BussinessService", "modal_info"]
function AddRepositoryModalInstanceCtrl($scope, $modalInstance, BussinessService, modal_info){
	$scope.modal_info = modal_info;

	$scope.ok = function(){
		var postData = {
			repository_info: $scope.formData
		}

		var postUrl = "/api/add_repository"

		BussinessService.list(postData, postUrl).success(function(response){
			swal({
				title: '缓存代码', text: response.result, type: "success", timer: 1500,
				showConfirmButton: false,
			});
			modal_info.GetTableRows();
			$modalInstance.close();
		})
		.error(function(response){
			swal({
				title: '缓存代码', text: response.result, type: "error", timer: 1500,
				showConfirmButton: false,
			});
			$modalInstance.close();
		})

	}

	$scope.cancel = function(){
		$modalInstance.dismiss('cancel');
	}
}
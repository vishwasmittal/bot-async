# from .api import device, account, location, report, job, jobrun
from aiohttp import web

from app.telegram.api import telegram_handler


async def index(request):
    return web.json_response({"version": "1.0.0"})


# def _setup_device_routes(app):
#     app.router.add_get('/api/redseer/v1/devices', device.get_devices)
#     app.router.add_get('/api/redseer/v1/devices/{deviceId}', device.get_device_detail)
#
#     app.router.add_post('/api/redseer/v1/devices', device.create_device)
#     app.router.add_put('/api/redseer/v1/devices/{deviceId}', device.edit_device)
#     app.router.add_delete('/api/redseer/v1/devices/{deviceId}', device.delete_device)
#
#
# def _setup_account_routes(app):
#     app.router.add_get('/api/redseer/v1/accounts', account.get_accounts)
#     app.router.add_get('/api/redseer/v1/accounts/{accountId}', account.get_account_detail)
#
#     app.router.add_post('/api/redseer/v1/accounts', account.create_account)
#     app.router.add_put('/api/redseer/v1/accounts/{accountId}', account.edit_account)
#     app.router.add_delete('/api/redseer/v1/accounts/{accountId}', account.delete_account)
#
#
# def _setup_location_routes(app):
#     app.router.add_get('/api/redseer/v1/locations', location.get_locations, name='location.get')
#     app.router.add_get('/api/redseer/v1/locations/{locationId}', location.get_location_detail)
#
#     app.router.add_post('/api/redseer/v1/locations', location.create_location, name='location.create')
#     app.router.add_put('/api/redseer/v1/locations/{locationId}', location.edit_location)
#     app.router.add_delete('/api/redseer/v1/locations/{locationId}', location.delete_location)
#
#
# def _setup_report_routes(app):
#     app.router.add_get('/api/redseer/v1/reports/download', report.get_report_download)
#     # app.router.add_post('/api/redseer/v1/reports', report.create_report)
#     # Delete
#     # app.router.add_delete('/api/redseer/v1/reports/{reportId}', report.delete_report)
#
#
# def _setup_jobrun_routes(app):
#     app.router.add_get('/api/redseer/v1/jobrun', jobrun.get_jobruns)
#     # app.router.add_get('/api/redseer/v1/jobrun/{jobrunId}/download', jobrun.get_jobrun_download)
#     app.router.add_get('/api/redseer/v1/jobrun/{jobrunId}', jobrun.get_jobrun_detail)
#     # app.router.add_post('/api/redseer/v1/jobrun', jobrun.create_jobrun)
#     # Delete
#     # app.router.add_delete('/api/redseer/v1/jobrun/{jobrunId}', jobrun.delete_jobrun)
#
#
# def _setup_jobs_routes(app):
#     app.router.add_get('/api/redseer/v1/jobs/{jobId}/run', job.run_job)
#     app.router.add_get('/api/redseer/v1/jobs/{jobId}', job.get_job_detail)
#     app.router.add_get('/api/redseer/v1/jobs', job.get_jobs)
#
#     app.router.add_post('/api/redseer/v1/jobs', job.create_job)
#     app.router.add_delete('/api/redseer/v1/jobs/{jobId}', job.delete_job)
#
#
# def setup_routes(app):
#     app.router.add_get('/', index)
#     # Setup device routes
#     _setup_device_routes(app)
#     _setup_account_routes(app)
#     _setup_location_routes(app)
#     _setup_jobs_routes(app)
#     _setup_jobrun_routes(app)
#     _setup_report_routes(app)

def _setup_jobs_routes(app):
    app.router.add_post('/job/', telegram_handler.handler)


def setup_routes(app):
    app.router.add_get('/', index)
    _setup_jobs_routes(app)

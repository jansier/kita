from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .forms import CalibrateMapForm
import cv2
import numpy as np
from PIL import Image
import tempfile

def index(request):
    if request.method == 'POST':
        # calibrate
        form = CalibrateMapForm(request.POST)
        if form.is_valid():
            tmp_file = tempfile.NamedTemporaryFile(suffix='.tif')
            tmp_file.write(request.FILES['map_file'].file.read())
            im_src = cv2.imread(tmp_file.name)

            pts_src = np.array([
                (form.cleaned_data['p1x'], form.cleaned_data['p1y']),
                (form.cleaned_data['p2x'], form.cleaned_data['p2y']),
                (form.cleaned_data['p3x'], form.cleaned_data['p3y']),
                (form.cleaned_data['p4x'], form.cleaned_data['p4y'])
            ])
            edge = pts_src[1]-pts_src[0]
            edge_vert = np.array((-edge[1], edge[0]))
            pts_dst = np.array([
                pts_src[0],
                pts_src[1],
                pts_src[1]-edge_vert,
                pts_src[0]-edge_vert,
            ])

            h, _ = cv2.findHomography(pts_src, pts_dst)
            im_dst = cv2.warpPerspective(im_src, h, (im_src.shape[1], im_src.shape[0]), borderValue=(255,255,255))
            Image.fromarray(im_dst).save(tmp_file.name, compression='tiff_deflate')
            tmp_file.seek(0)

            response = HttpResponse(tmp_file.read(), content_type='image/tiff')
            response['Content-Disposition'] = f'attachment; filename="{request.FILES["map_file"].name}"'

            return response

    return render(request, 'calibration/index.html', {'form': CalibrateMapForm()})


# Copyright 2016-2018 Euratom
# Copyright 2016-2018 United Kingdom Atomic Energy Authority
# Copyright 2016-2018 Centro de Investigaciones Energéticas, Medioambientales y Tecnológicas
#
# Licensed under the EUPL, Version 1.1 or – as soon they will be approved by the
# European Commission - subsequent versions of the EUPL (the "Licence");
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at:
#
# https://joinup.ec.europa.eu/software/page/eupl5
#
# Unless required by applicable law or agreed to in writing, software distributed
# under the Licence is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied.
#
# See the Licence for the specific language governing permissions and limitations
# under the Licence.

from numpy import ndarray
import matplotlib.pyplot as plt
from raysect.core import Node, translate, rotate_basis, Point3D, Vector3D
from raysect.optical import Spectrum
from raysect.optical.observer import FibreOptic, SightLine
from raysect.optical.observer import SpectralRadiancePipeline0D, SpectralPowerPipeline0D, RadiancePipeline0D, PowerPipeline0D


class Observer0DGroup(Node):
    """
    A base class for a group of 0D spectroscopic observers under a single scene-graph node.

    A scene-graph object regrouping a series of observers as a scene-graph parent.
    Allows combined observation and display control simultaneously.
    """

    def __init__(self, parent=None, transform=None, name=None):
        super().__init__(parent=parent, transform=transform, name=name)

        self._sight_lines = tuple()

    def __getitem__(self, item):

        if isinstance(item, int):
            try:
                return self._sight_lines[item]
            except IndexError:
                raise IndexError("Sight-line number {} not available in this {} "
                                 "with only {} sight-lines.".format(item, self.__class__.__name__, len(self._sight_lines)))
        elif isinstance(item, str):
            sightlines = [sight_line for sight_line in self._sight_lines if sight_line.name == item]
            if len(sightlines) == 1:
                return sightlines[0]

            if len(sightlines) == 0:
                raise ValueError("Sight-line '{}' was not found in this {}.".format(item, self.__class__.__name__))

            raise ValueError("Found {} sight-lines with name {} in this {}.".format(len(sightlines), item, self.__class__.__name__))
        else:
            raise TypeError("{} key must be of type int or str.".format(self.__class__.__name__))

    @property
    def names(self):
        """
        A list of sight-line names.

        :rtype: list
        """
        return [sight_line.name for sight_line in self._sight_lines]

    @names.setter
    def names(self, value):
        if isinstance(value, (list, tuple)):
            if len(value) == len(self._sight_lines):
                for sight_line, v in zip(self._sight_lines, value):
                    sight_line.name = v
            else:
                raise ValueError("The length of 'names' ({}) "
                                 "mismatches the number of sight-lines ({}).".format(len(value), len(self._sight_lines)))
        else:
            raise TypeError("The names attribute must be a list or tuple.")

    @property
    def origin(self):
        """
        The origin points for the sight lines.

        The same value can be shared between all sight lines,
        or each sight line can be assigned with individual value.

        :rtype: list
        """
        return [sight_line.origin for sight_line in self._sight_lines]

    @origin.setter
    def origin(self, value):
        if isinstance(value, (list, tuple)):
            if len(value) == len(self._sight_lines):
                for sight_line, v in zip(self._sight_lines, value):
                    sight_line.origin = v
            else:
                raise ValueError("The length of 'origin' ({}) "
                                 "mismatches the number of sight-lines ({}).".format(len(value), len(self._sight_lines)))
        else:
            for sight_line in self._sight_lines:
                sight_line.origin = value

    @property
    def direction(self):
        """
        The observation directions for the sight lines.

        The same value can be shared between all sight lines,
        or each sight line can be assigned with individual value.

        :rtype: list
        """
        return [sight_line.direction for sight_line in self._sight_lines]

    @direction.setter
    def direction(self, value):
        if isinstance(value, (list, tuple)):
            if len(value) == len(self._sight_lines):
                for sight_line, v in zip(self._sight_lines, value):
                    sight_line.direction = v
            else:
                raise ValueError("The length of 'direction' ({}) "
                                 "mismatches the number of sight-lines ({}).".format(len(value), len(self._sight_lines)))
        else:
            for sight_line in self._sight_lines:
                sight_line.direction = value

    @property
    def display_progress(self):
        """
        Toggles the display of live render progress.

        The same value can be shared between all sight lines,
        or each sight line can be assigned with individual value.

        :rtype: list
        """
        return [sight_line.display_progress for sight_line in self._sight_lines]

    @display_progress.setter
    def display_progress(self, value):
        if isinstance(value, (list, tuple, ndarray)):
            if len(value) == len(self._sight_lines):
                for sight_line, v in zip(self._sight_lines, value):
                    sight_line.display_progress = v
            else:
                raise ValueError("The length of 'display_progress' ({}) "
                                 "mismatches the number of sight-lines ({}).".format(len(value), len(self._sight_lines)))
        else:
            for sight_line in self._sight_lines:
                sight_line.display_progress = value

    @property
    def accumulate(self):
        """
        Toggles whether to accumulate samples with subsequent calls to observe().

        The same value can be shared between all sight lines,
        or each sight line can be assigned with individual value.

        :rtype: list
        """
        return [sight_line.accumulate for sight_line in self._sight_lines]

    @accumulate.setter
    def accumulate(self, value):
        if isinstance(value, (list, tuple, ndarray)):
            if len(value) == len(self._sight_lines):
                for sight_line, v in zip(self._sight_lines, value):
                    sight_line.accumulate = v
            else:
                raise ValueError("The length of 'accumulate' ({}) "
                                 "mismatches the number of sight-lines ({}).".format(len(value), len(self._sight_lines)))
        else:
            for sight_line in self._sight_lines:
                sight_line.accumulate = value

    @property
    def min_wavelength(self):
        """
        Lower wavelength bound for sampled spectral range.

        The same value can be shared between all sight lines,
        or each sight line can be assigned with individual value.

        :rtype: list
        """
        return [sight_line.min_wavelength for sight_line in self._sight_lines]

    @min_wavelength.setter
    def min_wavelength(self, value):
        if isinstance(value, (list, tuple, ndarray)):
            if len(value) == len(self._sight_lines):
                for sight_line, v in zip(self._sight_lines, value):
                    sight_line.min_wavelength = v
            else:
                raise ValueError("The length of 'min_wavelength' ({}) "
                                 "mismatches the number of sight-lines ({}).".format(len(value), len(self._sight_lines)))
        else:
            for sight_line in self._sight_lines:
                sight_line.min_wavelength = value

    @property
    def max_wavelength(self):
        """
        Upper wavelength bound for sampled spectral range.

        The same value can be shared between all sight lines,
        or each sight line can be assigned with individual value.

        :rtype: list
        """
        return [sight_line.max_wavelength for sight_line in self._sight_lines]

    @max_wavelength.setter
    def max_wavelength(self, value):
        if isinstance(value, (list, tuple, ndarray)):
            if len(value) == len(self._sight_lines):
                for sight_line, v in zip(self._sight_lines, value):
                    sight_line.max_wavelength = v
            else:
                raise ValueError("The length of 'max_wavelength' ({}) "
                                 "mismatches the number of sight-lines ({}).".format(len(value), len(self._sight_lines)))
        else:
            for sight_line in self._sight_lines:
                sight_line.max_wavelength = value

    @property
    def spectral_bins(self):
        """
        The number of spectral samples over the wavelength range.

        The same value can be shared between all sight lines,
        or each sight line can be assigned with individual value.

        :rtype: list
        """
        return [sight_line.spectral_bins for sight_line in self._sight_lines]

    @spectral_bins.setter
    def spectral_bins(self, value):
        if isinstance(value, (list, tuple, ndarray)):
            if len(value) == len(self._sight_lines):
                for sight_line, v in zip(self._sight_lines, value):
                    sight_line.spectral_bins = v
            else:
                raise ValueError("The length of 'spectral_bins' ({}) "
                                 "mismatches the number of sight-lines ({}).".format(len(value), len(self._sight_lines)))
        else:
            for sight_line in self._sight_lines:
                sight_line.spectral_bins = value

    @property
    def ray_extinction_prob(self):
        """
        Probability of ray extinction after every material intersection.

        The same value can be shared between all sight lines,
        or each sight line can be assigned with individual value.

        :rtype: list
        """
        return [sight_line.ray_extinction_prob for sight_line in self._sight_lines]

    @ray_extinction_prob.setter
    def ray_extinction_prob(self, value):
        if isinstance(value, (list, tuple, ndarray)):
            if len(value) == len(self._sight_lines):
                for sight_line, v in zip(self._sight_lines, value):
                    sight_line.ray_extinction_prob = v
            else:
                raise ValueError("The length of 'ray_extinction_prob' ({}) "
                                 "mismatches the number of sight-lines ({}).".format(len(value), len(self._sight_lines)))
        else:
            for sight_line in self._sight_lines:
                sight_line.ray_extinction_prob = value

    @property
    def ray_extinction_min_depth(self):
        """
        Minimum number of paths before russian roulette style ray extinction.

        The same value can be shared between all sight lines,
        or each sight line can be assigned with individual value.

        :rtype: list
        """
        return [sight_line.ray_extinction_min_depth for sight_line in self._sight_lines]

    @ray_extinction_min_depth.setter
    def ray_extinction_min_depth(self, value):
        if isinstance(value, (list, tuple, ndarray)):
            if len(value) == len(self._sight_lines):
                for sight_line, v in zip(self._sight_lines, value):
                    sight_line.ray_extinction_min_depth = v
            else:
                raise ValueError("The length of 'ray_extinction_min_depth' ({}) "
                                 "mismatches the number of sight-lines ({}).".format(len(value), len(self._sight_lines)))
        else:
            for sight_line in self._sight_lines:
                sight_line.ray_extinction_min_depth = value

    @property
    def ray_max_depth(self):
        """
        Maximum number of Ray paths before terminating Ray.

        The same value can be shared between all sight lines,
        or each sight line can be assigned with individual value.

        :rtype: list
        """
        return [sight_line.ray_max_depth for sight_line in self._sight_lines]

    @ray_max_depth.setter
    def ray_max_depth(self, value):
        if isinstance(value, (list, tuple, ndarray)):
            if len(value) == len(self._sight_lines):
                for sight_line, v in zip(self._sight_lines, value):
                    sight_line.ray_max_depth = v
            else:
                raise ValueError("The length of 'ray_max_depth' ({}) "
                                 "mismatches the number of sight-lines ({}).".format(len(value), len(self._sight_lines)))
        else:
            for sight_line in self._sight_lines:
                sight_line.ray_max_depth = value

    @property
    def ray_important_path_weight(self):
        """
        Relative weight of important path sampling.

        The same value can be shared between all sight lines,
        or each sight line can be assigned with individual value.

        :rtype: list
        """
        return [sight_line.ray_important_path_weight for sight_line in self._sight_lines]

    @ray_important_path_weight.setter
    def ray_important_path_weight(self, value):
        if isinstance(value, (list, tuple, ndarray)):
            if len(value) == len(self._sight_lines):
                for sight_line, v in zip(self._sight_lines, value):
                    sight_line.ray_important_path_weight = v
            else:
                raise ValueError("The length of 'ray_important_path_weight' ({}) "
                                 "mismatches the number of sight-lines ({}).".format(len(value), len(self._sight_lines)))
        else:
            for sight_line in self._sight_lines:
                sight_line.ray_important_path_weight = value

    @property
    def pixel_samples(self):
        """
        The number of samples to take per pixel.

        The same value can be shared between all sight lines,
        or each sight line can be assigned with individual value.

        :rtype: list
        """
        return [sight_line.pixel_samples for sight_line in self._sight_lines]

    @pixel_samples.setter
    def pixel_samples(self, value):
        if isinstance(value, (list, tuple, ndarray)):
            if len(value) == len(self._sight_lines):
                for sight_line, v in zip(self._sight_lines, value):
                    sight_line.pixel_samples = v
            else:
                raise ValueError("The length of 'pixel_samples' ({}) "
                                 "mismatches the number of sight-lines ({}).".format(len(value), len(self._sight_lines)))
        else:
            for sight_line in self._sight_lines:
                sight_line.pixel_samples = value

    @property
    def samples_per_task(self):
        """
        Minimum number of samples to request per task.

        The same value can be shared between all sight lines,
        or each sight line can be assigned with individual value.

        :rtype: list
        """
        return [sight_line.samples_per_task for sight_line in self._sight_lines]

    @samples_per_task.setter
    def samples_per_task(self, value):
        if isinstance(value, (list, tuple, ndarray)):
            if len(value) == len(self._sight_lines):
                for sight_line, v in zip(self._sight_lines, value):
                    sight_line.samples_per_task = v
            else:
                raise ValueError("The length of 'samples_per_task' ({}) "
                                 "mismatches the number of sight-lines ({}).".format(len(value), len(self._sight_lines)))
        else:
            for sight_line in self._sight_lines:
                sight_line.samples_per_task = value

    @property
    def pipelines(self):
        """
        List of all pipelines connected to each sight-line in the group
        """

        return [sight_line.pipelines for sight_line in self._sight_lines]

    def connect_pipelines(self, properties=[(SpectralRadiancePipeline0D, None, None)]):
        """
        Connects pipelines of given kinds and names to each sight-line in the group.
        Connected pipelines are non-accumulating by default.

        :param list properties: 3-tuple list of pipeline properties in order (class, name, filter).
                                Default is [(SpectralRadiancePipeline0D, None, None)].
                                The following pipeline classes are supported:
                                    SpectralRadiacnePipeline0D,
                                    SpectralPowerPipeline0D,
                                    RadiacnePipeline0D,
                                    PowerPipeline0D.
                                Filters are applied to the mono pipelines only, namely,
                                PowerPipeline0D or RadiacnePipeline0D. The values provided for spectral
                                pipelines will be ignored. The filter must be an instance of
                                SpectralFunction or None.

        """

        for sight_line in self._sight_lines:
            pipelines = []
            for PipelineClass, name, filter_func in properties:
                if PipelineClass in (SpectralRadiancePipeline0D, SpectralPowerPipeline0D):
                    pipelines.append(PipelineClass(accumulate=False, name=name))
                elif PipelineClass in (RadiancePipeline0D, PowerPipeline0D):
                    pipelines.append(PipelineClass(filter=filter_func, accumulate=False, name=name))
                else:
                    raise ValueError("Unsupported pipeline class: {}. "
                                     "Only the following pipeline types are supported: "
                                     "SpectralRadiancePipeline0D, SpectralPowerPipeline0D, "
                                     "RadiancePipeline0D, PowerPipeline0D.".format(PipelineClass.__name__))
            sight_line.pipelines = pipelines

    def observe(self):
        for sight_line in self._sight_lines:
            sight_line.observe()

    def plot_spectra(self, item=0, unit='J', ymax=None):
        """
        Plot the spectra observed by each line of sight in the group for a given pipeline.

        :param item: The index or name of the pipeline. Default: 0.
        :param str unit: Plots the spectrum in J/s (units='J'),
                         or in ph/s (units='ph').
        :param float ymax: Upper limit of y-axis.
        """

        pipelines = []
        sight_lines = []
        for sight_line in self.sight_lines:
            try:
                pipelines.append(sight_line.get_pipeline(item))
            except (ValueError, IndexError):
                continue
            else:
                sight_lines.append(sight_line)

        if len(pipelines) == 0:
            raise ValueError("Pipeline {} was not found for any sight-line in this {}.".format((item, self.__class__.__name__)))

        pipeline_types = set(type(pipeline) for pipeline in pipelines)
        if len(pipeline_types) > 1:
            raise ValueError("Pipelines {} have different types for different sight-lines.".format(item))

        plt.figure()
        for sight_line in sight_lines:
            sight_line.plot_spectra(item=item, unit=unit, extras=False)

        pipeline = pipelines[0]
        # RadiancePipelines are the instances of PowerPipelines, so they need to be checked first
        if isinstance(pipeline, RadiancePipeline0D):
            units = '{}/s/m^2/str'.format(unit)
        elif isinstance(pipeline, PowerPipeline0D):
            units = '{}/s'.format(unit)
        elif isinstance(pipeline, SpectralRadiancePipeline0D):
            units = '{}/s/m^2/str/nm'.format(unit)
        elif isinstance(pipeline, SpectralPowerPipeline0D):
            units = '{}/s/nm'.format(unit)
        else:
            units = ''

        if ymax is not None:
            plt.ylim(ymax=ymax)

        if isinstance(item, int):
            # check if pipelines share the same name
            if len(set(pipeline.name for pipeline in pipelines)) == 1:
                plt.title('{}: {}'.format(self.name, pipelines[0].name))
            else:
                # pipelines have different names
                plt.title('{}: pipeline {}'.format(self.name, item))
        elif isinstance(item, str):
            plt.title('{}: {}'.format(self.name, item))

        plt.xlabel('wavelength (nm)')
        plt.ylabel('radiance ({})'.format(units))
        plt.legend()


class LineOfSightGroup(Observer0DGroup):
    """
    A group of spectroscopic sight-lines under a single scene-graph node.

    A scene-graph object regrouping a series of 'SpectroscopicSightLine'
    observers as a scene-graph parent. Allows combined observation and display
    control simultaneously.
    """

    @property
    def sight_lines(self):
        return self._sight_lines

    @sight_lines.setter
    def sight_lines(self, value):

        if not isinstance(value, (list, tuple)):
            raise TypeError("The sight_lines attribute of LineOfSightGroup must be a list or tuple of SpectroscopicSightLines.")

        for sight_line in value:
            if not isinstance(sight_line, SpectroscopicSightLine):
                raise TypeError("The sight_lines attribute of LineOfSightGroup must be a list or tuple of "
                                "SpectroscopicSightLines. Value {} is not a SpectroscopicSightLine.".format(sight_line))

        # Prevent external changes being made to this list
        for sight_line in value:
            sight_line.parent = self

        self._sight_lines = tuple(value)

    def add_sight_line(self, sight_line):

        if not isinstance(sight_line, SpectroscopicSightLine):
            raise TypeError("The sight_line argument must be of type SpectroscopicSightLine.")

        sight_line.parent = self
        self._sight_lines = self._sight_lines + (sight_line,)


class FibreOpticGroup(Observer0DGroup):
    """
    A group of fibre optics under a single scene-graph node.

    A scene-graph object regrouping a series of 'SpectroscopicFibreOptic'
    observers as a scene-graph parent. Allows combined observation and display
    control simultaneously.
    """

    @property
    def sight_lines(self):
        return self._sight_lines

    @sight_lines.setter
    def sight_lines(self, value):

        if not isinstance(value, (list, tuple)):
            raise TypeError("The sight_lines attribute of FibreOpticGroup must be a list or tuple of SpectroscopicFibreOptics.")

        for sight_line in value:
            if not isinstance(sight_line, SpectroscopicFibreOptic):
                raise TypeError("The sight_lines attribute of FibreOpticGroup must be a list or tuple of "
                                "SpectroscopicFibreOptics. Value {} is not a SpectroscopicFibreOptic.".format(sight_line))

        # Prevent external changes being made to this list
        for sight_line in value:
            sight_line.parent = self

        self._sight_lines = tuple(value)

    def add_sight_line(self, sight_line):

        if not isinstance(sight_line, SpectroscopicFibreOptic):
            raise TypeError("The sightline argument must be of type SpectroscopicFibreOptic.")

        sight_line.parent = self
        self._sight_lines = self._sight_lines + (sight_line,)

    @property
    def acceptance_angle(self):
        """
        The angle in degrees between the z axis and the cone surface which defines the fibres
        solid angle sampling area.

        The same value can be shared between all sight lines,
        or each sight line can be assigned with individual value.

        :rtype: list
        """
        return [sight_line.acceptance_angle for sight_line in self._sight_lines]

    @acceptance_angle.setter
    def acceptance_angle(self, value):
        if isinstance(value, (list, tuple, ndarray)):
            if len(value) == len(self._sight_lines):
                for sight_line, v in zip(self._sight_lines, value):
                    sight_line.acceptance_angle = v
            else:
                raise ValueError("The length of 'acceptance_angle' ({}) "
                                 "mismatches the number of sight-lines ({}).".format(len(value), len(self._sight_lines)))
        else:
            for sight_line in self._sight_lines:
                sight_line.acceptance_angle = value

    @property
    def radius(self):
        """
        The radius of the fibre tip in metres. This radius defines a circular area at the fibre tip
        which will be sampled over.

        The same value can be shared between all sight lines,
        or each sight line can be assigned with individual value.

        :rtype: list
        """
        return [sight_line.radius for sight_line in self._sight_lines]

    @radius.setter
    def radius(self, value):
        if isinstance(value, (list, tuple, ndarray)):
            if len(value) == len(self._sight_lines):
                for sight_line, v in zip(self._sight_lines, value):
                    sight_line.radius = v
            else:
                raise ValueError("The length of 'radius' ({}) "
                                 "mismatches the number of sight-lines ({}).".format(len(value), len(self._sight_lines)))
        else:
            for sight_line in self._sight_lines:
                sight_line.radius = value


class _SpectroscopicObserver0DBase:
    """A base class for spectroscopic 0D observers."""

    @property
    def origin(self):
        """
        The origin point of the sight line.

        :rtype: Point3D
        """
        return self._origin

    @origin.setter
    def origin(self, value):
        if not isinstance(value, Point3D):
            raise TypeError("Attribute 'origin' must be of type Point3D.")

        if self._direction.x != 0 or self._direction.y != 0 or self._direction.z != 1:
            up = Vector3D(0, 0, 1)
        else:
            up = Vector3D(1, 0, 0)
        self._origin = value
        self.transform = translate(value.x, value.y, value.z) * rotate_basis(self._direction, up)

    @property
    def direction(self):
        """
        The observation direction of the sight line.

        :rtype: Vector3D
        """
        return self._direction

    @direction.setter
    def direction(self, value):
        if not isinstance(value, Vector3D):
            raise TypeError("Attribute 'direction' must be of type Vector3D.")

        if value.x != 0 or value.y != 0 or value.z != 1:
            up = Vector3D(0, 0, 1)
        else:
            up = Vector3D(1, 0, 0)
        self._direction = value
        self.transform = translate(self._origin.x, self._origin.y, self._origin.z) * rotate_basis(value, up)

    @property
    def display_progress(self):
        """ Toggles the display of live render progress."""
        display_progress_list = []
        for pipeline in self.pipelines:
            if isinstance(pipeline, SpectralPowerPipeline0D):
                display_progress_list.append(pipeline.display_progress)
            else:
                display_progress_list.append(None)
        return display_progress_list

    @display_progress.setter
    def display_progress(self, value):
        for pipeline in self.pipelines:
            if isinstance(pipeline, SpectralPowerPipeline0D):
                pipeline.display_progress = value

    @property
    def accumulate(self):
        """ Toggles whether to accumulate samples with subsequent calls to observe()."""
        accumulate_list = []
        for pipeline in self.pipelines:
            if isinstance(pipeline, (PowerPipeline0D, SpectralPowerPipeline0D)):
                accumulate_list.append(pipeline.accumulate)
            else:
                accumulate_list.append(None)
        return accumulate_list

    @accumulate.setter
    def accumulate(self, value):
        for pipeline in self.pipelines:
            if isinstance(pipeline, (PowerPipeline0D, SpectralPowerPipeline0D)):
                pipeline.accumulate = value

    def get_pipeline(self, item=0):
        if isinstance(item, int):
            try:
                return self.pipelines[item]
            except IndexError:
                raise IndexError("Pipeline number {} not available in this {} "
                                 "with only {} pipelines.".format(item, self.__class__.__name__, len(self.pipelines)))
        elif isinstance(item, str):
            pipelines = [pipeline for pipeline in self.pipelines if pipeline.name == item]
            if len(pipelines) == 1:
                return pipelines[0]

            if len(pipelines) == 0:
                raise ValueError("Pipeline '{}' was not found in this {}.".format(item, self.__class__.__name__))

            raise ValueError("Found {} pipelines with name {} in this {}.".format(len(pipelines), item, self.__class__.__name__))
        else:
            raise TypeError("{} key must be of type int or str.".format(self.__class__.__name__))

    def observed_spectrum(self, item=0):
        """
        Returns observed spectrum for a given pipeline.
        :param item: The index or name of the pipeline. Default: 0.

        :rtype: Spectrum
        """

        pipeline = self.get_pipeline(item)
        if isinstance(pipeline, PowerPipeline0D):
            spectrum = Spectrum(self.min_wavelength, self.max_wavelength, 1)
            spectrum.samples[0] = pipeline.value.mean / (self.max_wavelength - self.min_wavelength)
        elif isinstance(pipeline, SpectralPowerPipeline0D):
            if not pipeline.samples:
                raise ValueError("No spectrum has been observed.")
            spectrum = Spectrum(pipeline.min_wavelength, pipeline.max_wavelength, pipeline.bins)
            spectrum.samples = pipeline.samples.mean
        else:
            raise TypeError("Method 'observed_spectrum' supports only PowerPipeline0D, SpectralPowerPipeline0D and their instances. "
                            "Pipeline {} of type {} is not supported.".format(item, self.__class__.__name__))
        return spectrum

    def plot_spectra(self, item=0, unit='J', ymax=None, extras=True):
        """
        Plot the observed spectrum for a given pipeline.

        :param item: The index or name of the pipeline. Default: 0.
        :param str unit: Plots the spectrum in J/s (units='J'),
                         or in ph/s (units='ph').
        :param float ymax: Upper limit of y-axis.
        :param bool extras: If True, set title, axis labels and ymax.
        """

        if unit == 'J':
            # Spectrum objects are already in J/s
            spectrum = self.observed_spectrum(item)
        elif unit == 'ph':
            # turn the samples into ph/s
            spectrum_observed = self.observed_spectrum(item)
            spectrum = spectrum_observed.new_spectrum()
            spectrum.samples = spectrum_observed.to_photons()
        else:
            raise ValueError("unit must be 'J' or 'ph'.")

        if spectrum.samples.size > 1:
            plt.plot(spectrum.wavelengths, spectrum.samples, label=self.name)
        else:
            pipeline = self.get_pipeline(item)
            if isinstance(pipeline, SpectralPowerPipeline0D):
                plt.plot(spectrum.wavelengths, spectrum.samples, marker='o', ls='none', label=self.name)
            elif isinstance(pipeline, PowerPipeline0D):
                plt.plot(spectrum.wavelengths, spectrum.total(), marker='o', ls='none', label=self.name)

        if extras:
            pipeline = self.get_pipeline(item)
            # RadiancePipelines are the instances of PowerPipelines, so they need to be checked first
            if isinstance(pipeline, RadiancePipeline0D):
                units = '{}/s/m^2/str'.format(unit)
            elif isinstance(pipeline, PowerPipeline0D):
                units = '{}/s'.format(unit)
            elif isinstance(pipeline, SpectralRadiancePipeline0D):
                units = '{}/s/m^2/str/nm'.format(unit)
            elif isinstance(pipeline, SpectralPowerPipeline0D):
                units = '{}/s/nm'.format(unit)
            else:
                units = ''

            if ymax is not None:
                plt.ylim(ymax=ymax)

            plt.title('{}: {}'.format(self.name, pipeline.name))
            plt.xlabel('wavelength (nm)')
            plt.ylabel('radiance ({}})'.format(units))


class SpectroscopicSightLine(SightLine, _SpectroscopicObserver0DBase):

    """
    A simple line of sight observer.

    :param Point3D origin: The origin point for this sight-line.
    :param Vector3D direction: The observation direction for this sight-line.
    :param list pipelines: A list of pipelines that will process the resulting spectra
                           from this observer.
                           Default is [SpectralRadiancePipeline0D(accumulate=False)].
    """

    def __init__(self, origin, direction, pipelines=None, parent=None, name=None):

        self._origin = Point3D(0, 0, 0)
        self._direction = Vector3D(1, 0, 0)
        pipelines = pipelines or [SpectralRadiancePipeline0D(accumulate=False)]

        super().__init__(pipelines=pipelines, parent=parent, name=name)

        self.origin = origin
        self.direction = direction


class SpectroscopicFibreOptic(FibreOptic, _SpectroscopicObserver0DBase):

    """
    An optic fibre spectroscopic observer with non-zero acceptance angle.

    Rays are sampled over a circular area at the fibre tip and a conical solid angle
    defined by the acceptance_angle parameter.

    :param Point3D origin: The origin point for this sight-line.
    :param Vector3D direction: The observation direction for this sight-line.
    :param list pipelines: A list of pipelines that will process the resulting spectra
                           from this observer.
                           Default is [SpectralRadiancePipeline0D(accumulate=False)].
    :param float acceptance_angle: The angle in degrees between the z axis and the cone surface which defines the fibres
                                   solid angle sampling area.
    :param float radius: The radius of the fibre tip in metres. This radius defines a circular area at the fibre tip
                         which will be sampled over.
    """

    def __init__(self, origin, direction, pipelines=None, acceptance_angle=None, radius=None, parent=None, name=None):

        self._origin = Point3D(0, 0, 0)
        self._direction = Vector3D(1, 0, 0)
        pipelines = pipelines or [SpectralRadiancePipeline0D(accumulate=False)]

        super().__init__(pipelines=pipelines, parent=parent, name=name, acceptance_angle=acceptance_angle, radius=radius)

        self.origin = origin
        self.direction = direction
